import assert from 'node:assert/strict';
import { LiveApiAdapter } from '../services/adapters/liveApiAdapter';
import { ReportClient } from '../services/reportClient';
import { apiHeaders, resolveApiBaseUrl, setApiAccessKey } from '../services/apiConfig';
import { normalizeInspectionResponse } from '../services/adapters/responseNormalizer';

async function run() {
  const originalFetch = globalThis.fetch;
  let checks = 0;
  const check = (value: unknown, message: string) => { assert.ok(value, message); checks++; };
  const rejection = async (job: Promise<unknown>, code: string) => {
    await assert.rejects(job, (error: any) => error.code === code); checks++;
  };
  const image = new File([new Uint8Array([0xff,0xd8,0xff,0,0,0,0,0,0,0,0,0])], 'package.jpg', {type:'image/jpeg'});
  try {
    check(resolveApiBaseUrl('http://untrusted.example') === '', 'Remote cleartext API rejected');
    check(resolveApiBaseUrl('https://user:password@api.example') === '', 'Credentials in public URL rejected');
    check(resolveApiBaseUrl('https://api.example/?secret=x') === '', 'Query credentials rejected');
    check(resolveApiBaseUrl('https://api.example/') === 'https://api.example', 'HTTPS API allowed');
    setApiAccessKey(' local-test-only ');
    check(apiHeaders().Authorization === 'Bearer local-test-only', 'Explicit access key is attached');
    setApiAccessKey('');
    check(!apiHeaders().Authorization, 'Clearing access removes authorization');
    const adapter = new LiveApiAdapter('http://localhost:8000');
    let calls = 0;
    globalThis.fetch = (async (_input, init) => {
      calls++;
      const form = init?.body as FormData;
      check(form.getAll('file').length === 1 && !form.has('image'), 'Only one image sent');
      check((init?.headers as any).Authorization === 'Bearer local-test-only', 'Upload authorization present');
      return new Response('{}', {headers:{'content-type':'application/json'}});
    }) as typeof fetch;
    setApiAccessKey('local-test-only');
    await rejection(adapter.inspect(image), 'INVALID_SERVER_RESPONSE');
    const aborted = new AbortController(); aborted.abort();
    await rejection(adapter.inspect(image, {signal:aborted.signal}), 'TIMEOUT');
    check(calls === 1, 'Pre-canceled inspection sends no network request');
    globalThis.fetch = (async () => new Response('{"detail":"denied"}', {status:401})) as typeof fetch;
    await rejection(adapter.inspect(image), 'HTTP_400');
    globalThis.fetch = (async () => new Response('{"detail":"busy"}', {status:429})) as typeof fetch;
    await rejection(adapter.inspect(image), 'HTTP_400');
    await rejection(adapter.submitReview({inspectionId:'INSP-1',fieldName:'mrp',decision:'CONFIRMED'}), 'REVIEW_API_NOT_IMPLEMENTED');
    const model = normalizeInspectionResponse({inspection_id:'INSP-1',state:'MANUAL_REVIEW_REQUIRED', declarations:{net_quantity_value:200, net_quantity_unit:'g', declared_usp_value:1}, rule_evaluations:{font_height_audit:{status:'REVIEW',is_compliant:false},usp_audit:{status:'NOT_APPLICABLE',is_compliant:false}}});
    check(model.declarations.net_quantity.verdict === 'REVIEW', 'Unknown font measurement stays REVIEW');
    check(model.declarations.unit_sale_price.verdict === 'NOT_APPLICABLE', 'USP applicability preserved');
    check(model.declarations.net_quantity.confidence === null, 'Absent confidence is never invented');
    const cropModel = normalizeInspectionResponse({inspection_id:'INSP-2',state:'MANUAL_REVIEW_REQUIRED',declarations:{mrp_inr:100},evidence_crops:[{field_name:'mrp',label:'MRP & Tax Qualifier Crop',bbox_px:[0,0,100,30]}]});
    check(cropModel.ocrTokens.length === 0, 'Crop descriptions are not recognized text');
    check(cropModel.declarations.mrp.verdict === 'REVIEW', 'Presence alone cannot establish a rule pass');
    check(cropModel.evidenceItems[0].confidence === null, 'Crop confidence remains unknown when not supplied');
    const observedModel = normalizeInspectionResponse({inspection_id:'INSP-3',state:'MANUAL_REVIEW_REQUIRED',declarations:{country_of_origin:'India'},ocr_observations:[{token_id:'actual-1',text:'Made in India',confidence:0.91,bounding_box:{x_min:1,y_min:2,x_max:50,y_max:25}}]});
    check(observedModel.ocrTokens[0].text === 'Made in India' && observedModel.ocrTokens[0].confidence === 0.91, 'Actual recognized text and confidence are preserved');
    check(observedModel.declarations.country_of_origin.verdict === 'REVIEW', 'Detected origin without a rule result is not a rule pass');
    const report = new ReportClient('http://localhost:8000');
    await rejection(report.downloadAssessmentReport('../escape'), 'INVALID_INSPECTION_ID');
    await rejection(report.downloadAssessmentReport('INSP-1',{signal:aborted.signal}), 'CANCELED');
    let release!: (response: Response) => void;
    globalThis.fetch = (() => new Promise<Response>(resolve => {release=resolve;})) as typeof fetch;
    const cancel = new AbortController();
    const pending = report.downloadAssessmentReport('INSP-1',{signal:cancel.signal});
    await rejection(report.downloadAssessmentReport('INSP-2'), 'ALREADY_GENERATING');
    cancel.abort();
    release(new Response('%PDF-1.7\n',{headers:{'content-type':'application/pdf'}}));
    await rejection(pending, 'CANCELED');
    globalThis.fetch = (async () => new Response('%PDF-1.7\n',{headers:{'content-type':'application/pdf','content-disposition':"attachment; filename*=UTF-8''bad%ZZ.pdf"}})) as typeof fetch;
    const result = await report.downloadAssessmentReport('INSP-2');
    check(result.success && result.filename === 'bad_ZZ.pdf', 'Malformed download filename cannot crash generation');
    console.log(`Launch boundary tests: ${checks} passed`);
  } finally { globalThis.fetch=originalFetch; setApiAccessKey(''); }
}
run().catch(error => { console.error(error); process.exitCode=1; });
