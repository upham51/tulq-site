/* ══════════════════════════════════════════════════════════════════════
   awv-worksheet.js — the Annual Wellness Visit worksheet tool.

   Builds its UI from the SECTIONS model below, which is keyed to the
   elements of the annual wellness visit at 42 CFR 410.15. Runs entirely in
   the browser: no patient data is transmitted, and only operator details
   (nurse name, physician, practice) are persisted, in localStorage.

   Served immutable; the reference is hashed by tools/stamp-assets.py.
   ══════════════════════════════════════════════════════════════════════ */

(function(){
var $=function(i){return document.getElementById(i)};
var ROOT=document.querySelector('.awv-tool')||document;
var esc=function(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')};

/* ============ CONFIG ============
 set: 'both' = required in first and subsequent | 'first' = first visit only
 kind: 'update' shows a no-change control | 'assess' does not
 disc: discretionary element
=================================== */
var SECTIONS=[
{id:'hra',n:'Health risk assessment',cite:'(i)',set:'both',kind:'update',
 groups:[
 {id:'hraSource',t:'How it was collected',ask:'Confirm the assessment was completed. It may be completed by the patient in advance.',
  chips:['Completed by the patient in advance and reviewed today|Updated health risk assessment completed by the patient in advance and reviewed during this visit','Administered by the nurse during the visit|Updated health risk assessment administered by the nurse during this visit','Completed with help from a family member or caregiver']},
 {id:'hraFlags',t:'What the assessment flagged',ask:'Only follow up on what the form flagged. Do not re-interview the whole thing.',
  neg:'Assessment reviewed, nothing flagged for follow up',
  chips:['Low mood or loss of interest flagged|Assessment flagged low mood or loss of interest','Loneliness or isolation flagged|Assessment flagged loneliness or social isolation','Stress or anger flagged','Pain flagged','Fatigue flagged','Tobacco use flagged','Alcohol use flagged','Physical inactivity flagged','Nutrition concern flagged','Oral health concern flagged','Seat belt use flagged','Home safety concern flagged|Assessment flagged a home safety concern','Needs help with activities of daily living|Assessment flagged needing help with activities of daily living','Needs help with instrumental activities|Assessment flagged needing help with shopping, cooking, finances, or medications','Fall or balance concern flagged|Assessment flagged a fall or balance concern','Hearing concern flagged','Self rated health poor or fair']}
 ]},

{id:'history',n:'Medical and family history',cite:'(ii)',set:'both',kind:'update',
 groups:[
 {id:'chronicList',t:'Conditions treated for',ask:'Confirm the list. Anything new since last year?',
  chips:['High blood pressure','Type 2 diabetes','Heart failure','Coronary artery disease','Atrial fibrillation','COPD','Asthma','Chronic kidney disease','Stroke or TIA','Osteoarthritis','Osteoporosis','Depression','Anxiety','Hypothyroidism','GERD','Cancer history','Dementia or memory disorder','Peripheral neuropathy','Sleep apnea','Peripheral artery disease','Obesity','Chronic pain']},
 {id:'hxUpdate',t:'New since last visit',ask:'Any hospital stays, surgeries, injuries, new diagnoses, or new allergies this year?',
  neg:'No new illnesses, hospital stays, operations, injuries, or allergies since the last visit',
  chips:['Hospital stay this year|Reports a hospital stay since the last visit','Emergency visit this year','Surgery this year','New diagnosis this year','Injury or fall requiring care','New drug allergy','Stopped a treatment']},
 {id:'meds',t:'Medications and supplements',ask:'Confirm the list. Anything started, stopped, or changed? Do you ever skip because of cost or side effects? Who fills the pillbox?',
  neg:'Medication and supplement list reviewed, unchanged, no adherence concerns reported',
  chips:['Takes insulin','Oral diabetes medication','Anticoagulant or blood thinner','Diuretic','Inhaler or nebulizer','Antidepressant','Statin','Five or more medications','Ten or more medications','New medication this year','Stopped a medication this year','Uses a pillbox','Family member manages the pills|A family member manages the pills for the patient','Skips doses because of cost|Reports skipping doses because of cost','Skips doses because of side effects|Reports skipping doses because of side effects','Ran out recently|Reports running out of a medication recently','Takes over the counter products','Takes supplements']},
 {id:'hxFam',t:'Family history',ask:'Anything new in parents, siblings, or children this year?',
  neg:'Family history reviewed, unchanged',
  chips:['Heart disease','Stroke','Cancer','Diabetes','Dementia','Osteoporosis','New family event this year','Unknown, adopted or no contact']}
 ]},

{id:'providers',n:'Providers and suppliers',cite:'(iii)',set:'both',kind:'update',
 groups:[
 {id:'providers',t:'Specialists, services, and equipment',ask:'Confirm the list. Anyone new? Any new equipment or services at home?',
  neg:'Provider and supplier list reviewed, unchanged',
  chips:['Cardiologist','Nephrologist or kidney doctor|Sees a nephrologist, kidney doctor','Pulmonologist','Endocrinologist','Neurologist','Oncologist','Orthopedics','Urology','Ophthalmology','Podiatry','Behavioral health provider','Dialysis center','Home oxygen|Uses home oxygen','CPAP','Nebulizer','Walker|Uses a walker','Cane|Uses a cane','Wheelchair|Uses a wheelchair','Hospital bed','Bedside commode','Shower chair or grab bars','Glucose meter','Home blood pressure cuff|Has a home blood pressure cuff','Hearing aids','Home health agency','Physical or occupational therapy','Home health aide for personal care|A home health aide helps with bathing and dressing','Meal delivery','New provider this year','New equipment this year']}
 ]},

{id:'measure',n:'Measurements',cite:'(iv)',set:'both',kind:'assess',special:'measure',
 groups:[
 {id:'wtChange',t:'Weight change',ask:'Have your clothes gotten looser or tighter? Are you eating the way you normally do?',
  neg:'Weight stable over the past year',
  chips:['Reports losing weight|Reports losing weight without trying','Reports gaining weight','Clothes looser|Reports clothes have gotten looser','Not eating normally|Reports not eating the way they normally do','Unsure of prior weight']}
 ]},

{id:'cognitive',n:'Detection of cognitive impairment',cite:'(v)',set:'both',kind:'assess',special:'cog',
 groups:[
 {id:'cogObs',t:'Direct observation during the visit',ask:'The regulation defines this element as assessment by direct observation. Record what you observed.',
  neg:'No abnormality observed on direct observation during the visit',
  chips:['Gave a coherent history','Needed prompting for the history','Word finding difficulty observed|Word finding difficulty observed during the visit','Repeated questions during the visit|Repeated the same question during the visit','Oriented to time and place','Could not name current medications|Could not name their current medications','Deferred to a family member for answers','Lost track of the conversation|Lost track of the conversation at times']},
 {id:'cogReport',t:'Patient, family, or caregiver report',ask:'Any change in memory or thinking? To anyone present: repeating questions, missed appointments, trouble with bills or pills?',
  neg:'No concerns reported by the patient or anyone present',
  chips:['Patient reports memory change|Patient reports noticing a change in memory','Family reports repeating questions|Family reports the patient repeating questions','Family reports missed appointments|Family reports the patient missing appointments','Trouble managing the pills|Reports trouble managing the pills','Trouble managing bills or finances','Got lost or disoriented recently|Reports getting lost or disoriented recently','Family has taken over tasks this year','No informant available']}
 ]},

{id:'depression',n:'Depression risk, screening instrument',cite:'first visit (vi)',set:'first',kind:'assess',special:'phq',
 groups:[
 {id:'moodQuote',t:'Context and the patient\'s own words',ask:'Record what they said, whether the screen is positive or negative.',
  neg:'Denies low mood or loss of interest',
  chips:['Reports losing interest in things|Reports having lost interest in things they used to enjoy','Reports feeling down|Reports feeling down or low','Reports feeling lonely|Reports feeling lonely','Reports grief or recent loss','Currently in counseling','Treated for depression before','Mood described as usual for them']}
 ]},

{id:'function',n:'Functional ability and level of safety',cite:'first visit (vii)',set:'first',kind:'assess',
 groups:[
 {id:'adl',t:'Activities of daily living',ask:'Help with bathing, dressing, the toilet, transfers, eating? Shopping, cooking, housework, laundry, money, medicines, transportation?',
  neg:'Independent in all activities of daily living and instrumental activities',
  chips:['Needs help bathing','Needs help dressing','Needs help toileting','Needs help with transfers','Needs help eating','Needs help shopping','Needs help cooking','Needs help with housework','Needs help with laundry','Needs help managing money','Needs help managing medications','Needs help with transportation','Function declined this year|Reports function has declined over the past year']},
 {id:'fallDetail',t:'Fall risk',ask:'Fallen in the past year? Unsteady? Worry about falling? Dizzy standing up? Ever blacked out?',
  neg:'Three question falls screen negative on all three items',
  chips:['Fell in the past year|Reports a fall in the past year','Two or more falls','Injured in a fall','Emergency visit after a fall','Feels unsteady|Reports feeling unsteady standing or walking','Worries about falling|Reports worry about falling','Dizzy on standing|Reports getting dizzy or lightheaded on standing','Has passed out|Reports having passed out','Holds furniture to walk']},
 {id:'homeSafety',t:'Home safety',ask:'Stairs? Loose rugs? Grab bars? Lighting? If you fell, how would you call for help?',
  neg:'No home safety hazards identified',
  chips:['Stairs in the home','No grab bars in the bathroom','Loose rugs or cords','Poor lighting at night','No way to call for help if a fall occurs|Reports no way to call for help if they fell','Has a personal emergency alert device','Clutter or narrow pathways','Working smoke alarms']},
 {id:'hearVis',t:'Hearing impairment',ask:'Trouble hearing on the phone or in a group? Hearing aids?',
  neg:'No hearing impairment reported',
  chips:['Trouble hearing in a group','Trouble hearing on the phone','Wears hearing aids','Declines hearing evaluation','Vision change reported']}
 ]},

{id:'schedule',n:'Screening schedule and risk factor list',cite:'(vi)',set:'both',kind:'update',
 groups:[
 {id:'schedule',t:'Screenings and immunizations due',ask:'Last colonoscopy or stool test? Mammogram? Bone density? Dilated eye exam? Flu, pneumonia, shingles, tetanus, COVID, RSV?',
  neg:'Screening schedule reviewed and updated, nothing currently due',
  chips:['Colorectal cancer screening due','Mammogram due','Bone density scan due','Lung cancer screening to be assessed','Abdominal aortic aneurysm screening due','Hepatitis C screening due','Diabetes screening due','Lipid panel due','Dilated eye exam due','Dental visit due','Influenza vaccine due','Pneumococcal vaccine due','Shingles vaccine due','Tdap due','COVID vaccine due','RSV vaccine to be assessed']},
 {id:'riskList',t:'Risk factor and condition list update',ask:'Anything added or resolved since last year?',
  neg:'Risk factor and condition list reviewed and updated, no change',
  chips:['New risk factor added this year','A risk factor resolved this year','Intervention already underway','Treatment options and risks discussed']}
 ]},

{id:'advice',n:'Personalized health advice and referrals',cite:'(vii)',set:'both',kind:'assess',
 groups:[
 {id:'riskInt',t:'Advice given and referrals made',ask:'Every risk found today needs something next to it.',
  neg:'No new risks identified, prior plan reaffirmed',
  chips:['Falls prevention program referral','Home safety evaluation requested','Physical therapy referral','Dietitian referral','Diabetes education referral','Smoking cessation counseling offered','Behavioral health referral','Audiology referral','Ophthalmology referral','Medication review flagged for the physician','Care management enrollment discussed','Weight management discussed','Physical activity advice given','Nutrition advice given','Transportation resources provided','Food resources provided','Home blood pressure monitoring discussed']},
 {id:'agreed',t:'What the patient agreed to, in their words',ask:'Two or three, specific, said by the patient.',free:true,
  chips:['Will schedule the screening discussed','Will call about the referral','Will start walking regularly','Will bring all medications to the next visit','Will discuss the advance directive with family']}
 ]},

{id:'opioid',n:'Review of current opioid prescriptions',cite:'(ix)',set:'both',kind:'assess',gate:'opioid',
 groups:[
 {id:'opioid',t:'Required review content',ask:'Only applies where the chart shows a current opioid prescription. Risk factors, pain severity, treatment plan, non-opioid options, referral as appropriate.',
  chips:['Risk factors for opioid use disorder reviewed','Pain severity evaluated','Current treatment plan evaluated','Non-opioid treatment options provided','Referred to a specialist','Uses the opioid only as needed']}
 ]},

{id:'substance',n:'Screening for potential substance use disorders',cite:'(x)',set:'both',kind:'assess',
 groups:[
 {id:'substance',t:'Screen and risk factor review',ask:'How often do you have a drink containing alcohol? Do you use tobacco or nicotine? Anything else, including anything not prescribed to you?',
  neg:'Screened for potential substance use disorder, no risk factors identified, no referral indicated',
  chips:['Alcohol less than weekly','Alcohol weekly','Alcohol most days|Reports drinking most days','Six or more on one occasion at times|Reports six or more drinks on one occasion at times','Current smoker|Current smoker, smoking daily','Former smoker','Twenty or more pack years|Reports twenty or more pack years','Uses vape or e-cigarette','Uses cannabis','Uses a substance not prescribed to them','Risk factors identified','Referral for treatment offered','Referral declined','Interested in quitting']}
 ]},

{id:'acp',n:'Advance care planning',cite:'(viii), at beneficiary discretion',set:'both',kind:'assess',disc:true,
 groups:[
 {id:'acp',t:'Discussion',ask:'Have you thought about who would speak for you if you could not? Anything written down? Want to talk about it today?',
  neg:'Advance care planning offered, patient declined at their discretion',
  chips:['Has an advance directive on file','Has a healthcare proxy named','Discussion held today|Advance care planning discussion held today','Forms provided to complete','Wants to discuss with family first','Wishes documented in the chart']}
 ]},

{id:'panra',n:'Physical activity and nutrition risk assessment',cite:'(xi), discretionary, G0136',set:'both',kind:'assess',disc:true,
 groups:[
 {id:'panra',t:'Standardized assessment',ask:'Only when there is a known or suspected need. This is not a screening for every patient, and it carries patient cost sharing unless furnished with the wellness visit.',
  neg:'Not indicated today, no known or suspected physical activity or nutrition need',
  chips:['Standardized physical activity assessment administered','Standardized nutrition assessment administered','Known need related to physical activity','Known need related to nutrition','Results will adjust the treatment plan','Follow up arranged']}
 ]},

{id:'programs',n:'Program screening',cite:'not a required element',set:'both',kind:'assess',
 groups:[
 {id:'recentHosp',t:'Recent facility discharge',ask:'Hospital or rehab in the last month? When did you come home? Anyone called you since?',
  neg:'No facility discharge in the last thirty days',
  chips:['Hospital discharge in the last thirty days|Discharged from the hospital within the last thirty days','Observation stay','Skilled nursing facility discharge','Emergency department visit only','No follow up contact since discharge']},
 {id:'caregiver',t:'Caregiver situation',ask:'Anyone helping at home, with what? To the caregiver: anything you feel unprepared for?',
  neg:'No caregiver involved and none needed at this time',
  chips:['Spouse or partner provides care','Adult child provides care','Paid caregiver','Caregiver feels unprepared for some tasks|The caregiver reports feeling unprepared for some tasks','Caregiver reports it has gotten harder','Caregiver has no relief or backup']},
 {id:'monitorWilling',t:'Home monitoring',ask:'Cuff, scale, or glucose meter? Do you use it? Willing to if the office sees the readings?',
  neg:'No home monitoring and not interested at this time',
  chips:['Has a home blood pressure cuff|Has a home blood pressure monitor','Has a scale','Has a glucose meter','Uses the device regularly','Has a device but does not use it','Willing to use a monitor|Willing to use a home monitor if the office reviews the readings','Would need help setting a device up']},
 {id:'socialNeeds',t:'Social needs affecting the plan',ask:'Transportation, food, utilities, housing, safety. Recorded because it changes what plan is realistic, not as a billable element.',
  neg:'No unmet social needs identified',
  chips:['Lives alone','Reports isolation|Reports being isolated, few contacts in a normal week','No transportation to appointments|Reports no transportation, cannot get to appointments reliably','Cost concerns for food or medicine|Reports difficulty affording food or medicine','Housing concern','Utilities concern','Does not feel safe at home']},
 {id:'bhStatus',t:'Behavioral health treatment',ask:'Seeing anyone for mood, anxiety, or stress? Have you before? Want help?',
  neg:'No behavioral health treatment current or wanted',
  chips:['Currently seeing a counselor or therapist','Currently on a medication for mood or anxiety','Treated in the past','Would like a referral','Declines a referral']}
 ]},

{id:'esc',n:'Escalations and items for the physician',cite:'always complete',set:'both',kind:'assess',
 groups:[
 {id:'escImmediate',t:'Immediate escalations during the visit',ask:'Self harm content, acute symptoms, suspected abuse or neglect, acute confusion, unsafe situation right now.',
  neg:'None',
  chips:['Physician reached during the visit','Emergency services advised','Mandatory report initiated','Patient remained on the line until resolved']},
 {id:'escSameDay',t:'Same day items routed to the physician',ask:'Positive screens, falls, medication discrepancies, abnormal reported values.',
  neg:'None',
  chips:['Cognitive concern','Mood concern','Falls reported','Medication discrepancy','Abnormal reported blood pressure','Unexplained weight loss','No blood pressure value obtained']},
 {id:'newSymptom',t:'New symptoms or concerns raised',ask:'Document verbatim and route. Do not advise.',neg:'None',free:true,chips:[]}
 ]}
];

var consentChips=['Two identifiers confirmed','Private setting confirmed','Told this is not a physical exam','Told there is no cost','Verbal agreement to proceed','Physician availability confirmed'];

/* ============ RENDER ============ */
function parseChip(c){var p=c.split('|');return {label:p[0],phrase:p[1]||p[0]}}
function chipHtml(gid,c,isNeg){
 var o=parseChip(c);
 return '<label class="'+(isNeg?'neg':'')+'"><input type="checkbox" data-g="'+gid+'" data-t="'+o.phrase.replace(/"/g,'&quot;')+'"><span>'+esc(o.label)+'</span></label>';
}
function groupHtml(g){
 var h='<div class="gp"><div class="gt"><span>'+esc(g.t)+'</span><em data-clear="'+g.id+'">clear</em></div>';
 if(g.ask)h+='<p class="ask">'+esc(g.ask)+'</p>';
 h+='<div class="chips" id="chips-'+g.id+'">';
 if(g.neg)h+=chipHtml(g.id,g.neg,true);
 (g.chips||[]).forEach(function(c){h+=chipHtml(g.id,c,false)});
 h+='</div><textarea class="other" id="'+g.id+'_other" placeholder="'+(g.free?'The patient\'s own words':'Anything else, or the patient\'s own words')+'"></textarea></div>';
 return h;
}
var SPECIAL={
 measure:'<div class="row3">'+
  '<div><label class="fl" for="wt">Weight</label><input type="text" id="wt"></div>'+
  '<div><label class="fl" for="waist">Or waist circumference</label><input type="text" id="waist"></div>'+
  '<div id="htbmi"></div></div>'+
  '<div class="gp"><div class="gt"><span>Blood pressure, required element with no alternative</span></div>'+
  '<p class="ask">One of three outcomes. There is no fourth. A previously recorded value is never entered as though it were taken today.</p>'+
  '<div class="chips" id="chips-bpOutcome">'+
   '<label><input type="radio" name="bpOutcome" value="obtained"><span>Value obtained</span></label>'+
   '<label><input type="radio" name="bpOutcome" value="prior"><span>No device, most recent recorded value used</span></label>'+
   '<label><input type="radio" name="bpOutcome" value="declined"><span>Patient declined to take a reading</span></label>'+
  '</div>'+
  '<div class="row"><div><label class="fl" for="bp">Reading</label><input type="text" id="bp" placeholder="138/82"></div>'+
  '<div><label class="fl" for="bpSrc">Source</label><select id="bpSrc"><option value="">Select</option>'+
  '<option>measured in the office by clinic staff today</option>'+
  '<option>taken by the patient during this visit on a home device</option>'+
  '<option>reported by the patient from a home device</option>'+
  '<option>the most recent value recorded at the practice</option>'+
  '<option>taken at a pharmacy or community kiosk</option></select></div></div>'+
  '<div class="row"><div><label class="fl" for="bpDate">Date the value was taken</label><input type="text" id="bpDate" placeholder="Today, or 3 March 2026"></div>'+
  '<div><label class="fl" for="bpReason">Reason no reading today, if applicable</label><input type="text" id="bpReason" placeholder="No cuff at home"></div></div>'+
  '<div id="bpAlert"></div></div>',
 cog:'<div class="row"><div><label class="fl" for="cogTool">Standardized instrument, optional</label><select id="cogTool"><option value="">Not used, direct observation only</option>'+
  '<option>Mini-Cog</option><option>General Practitioner Assessment of Cognition</option><option>Memory Impairment Screen</option><option>Montreal Cognitive Assessment</option></select></div>'+
  '<div><label class="fl" for="cogScore">Score, if an instrument was used</label><input type="text" id="cogScore" placeholder="4 of 5"></div></div>',
 phq:'<div class="row"><div><label class="fl" for="phq1">Little interest or pleasure in doing things</label>'+
  '<select id="phq1" class="phq"><option value="">Select</option><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></div>'+
  '<div><label class="fl" for="phq2">Feeling down, depressed, or hopeless</label>'+
  '<select id="phq2" class="phq"><option value="">Select</option><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></div></div>'+
  '<p class="ask" id="phqScore">Two item total: not yet scored</p>'+
  '<div class="row"><div><label class="fl" for="phq9">Nine item total, if positive</label><input type="text" id="phq9" placeholder="11 of 27"></div>'+
  '<div><label class="fl" for="safetyItem">Self harm question, asked directly</label><select id="safetyItem"><option value="">Select</option>'+
  '<option>Asked, patient denies any such thoughts</option><option>POSITIVE, escalation protocol activated</option>'+
  '<option>Declined to answer, escalated to supervising physician</option></select></div></div>'
};
function sectionHtml(s){
 var h='<div class="sec" id="sec-'+s.id+'" data-set="'+s.set+'">'+
  '<div class="sech" data-toggle="'+s.id+'"><span class="tw">+</span>'+
  '<span class="nm">'+esc(s.n)+'</span>'+
  '<span class="cite">'+esc(s.cite)+'</span>'+
  '<span class="st" id="st-'+s.id+'">open</span></div>'+
  '<div class="secb" id="body-'+s.id+'" hidden>';
 h+='<div class="quick">';
 if(s.kind==='update')h+='<button data-quick="nochange" data-sec="'+s.id+'">No change since last visit</button>';
 h+='<button data-quick="normal" data-sec="'+s.id+'">Nothing abnormal</button>';
 h+='<button data-quick="declined" data-sec="'+s.id+'">Patient declined</button>';
 h+='<button data-quick="reset" data-sec="'+s.id+'">Reset</button>';
 h+='</div>';
 if(s.gate==='opioid')h+='<div class="gp"><div class="gt"><span>Does the chart show a current opioid prescription?</span></div>'+
  '<div class="chips" id="chips-opioidGate">'+
  '<label><input type="radio" name="opioidGate" value="no" checked><span>No current opioid prescription</span></label>'+
  '<label><input type="radio" name="opioidGate" value="yes"><span>Yes, current prescription</span></label></div></div>';
 if(s.special&&SPECIAL[s.special]&&s.special==='measure')h+=SPECIAL[s.special];
 s.groups.forEach(function(g){h+=groupHtml(g)});
 if(s.special&&SPECIAL[s.special]&&s.special!=='measure')h+=SPECIAL[s.special];
 h+='</div></div>';
 return h;
}
function build(){
 $('formHost').innerHTML=SECTIONS.map(sectionHtml).join('');
 var ch='<div class="gp"><div class="gt"><span>Consent and expectations</span><em data-clear="consent">clear</em></div><div class="chips" id="chips-consent">';
 consentChips.forEach(function(c){ch+=chipHtml('consent',c,false)});
 ch+='</div></div>';
 $('grp-consent').innerHTML=ch;
 $('htbmi').innerHTML='';
}
build();

/* ============ STATE ============ */
var secState={};
function chipsOf(g){var o=[];document.querySelectorAll('#chips-'+g+' input:checked').forEach(function(el){
 if(el.getAttribute('data-t'))o.push(el.getAttribute('data-t'))});return o}
function v(id){
 var el=$(id);
 if(el&&!document.getElementById('chips-'+id)&&(el.tagName==='INPUT'||el.tagName==='SELECT'||el.tagName==='TEXTAREA'))return (el.value||'').trim();
 var p=chipsOf(id);var o=$(id+'_other');
 if(o&&o.value.trim())p.push(o.value.trim());
 return p.join('. ');
}
function vtype(){return $('vtype').value}
function activeSections(){return SECTIONS.filter(function(s){return s.set==='both'||vtype()==='initial'})}
function isActive(s){return s.set==='both'||vtype()==='initial'}
function bpOutcome(){var e=document.querySelector('input[name=bpOutcome]:checked');return e?e.value:''}
function opioidGate(){var e=document.querySelector('input[name=opioidGate]:checked');return e?e.value:'no'}
function phqTotal(){var a=$('phq1'),b=$('phq2');if(!a||!b||a.value===''||b.value==='')return null;return parseInt(a.value,10)+parseInt(b.value,10)}
function chronicCount(){return chipsOf('chronicList').length+(($('chronicList_other')||{value:''}).value.trim()?1:0)}
function fmtDate(s){if(!s)return'';var p=s.split('-');if(p.length!==3)return s;
 var m=['January','February','March','April','May','June','July','August','September','October','November','December'];
 return parseInt(p[2],10)+' '+m[parseInt(p[1],10)-1]+' '+p[0]}
function secHasContent(s){
 return s.groups.some(function(g){return v(g.id)})}

/* ============ QUICK ACTIONS ============ */
function setSecState(id,st){secState[id]=st;refresh()}
function sectionById(id){for(var i=0;i<SECTIONS.length;i++)if(SECTIONS[i].id===id)return SECTIONS[i]}
function clearSection(s){
 s.groups.forEach(function(g){
  document.querySelectorAll('#chips-'+g.id+' input').forEach(function(el){el.checked=false});
  var o=$(g.id+'_other');if(o)o.value='';
 });
}
function applyNormal(s){
 clearSection(s);
 s.groups.forEach(function(g){
  if(!g.neg)return;
  var el=document.querySelector('#chips-'+g.id+' input');
  if(el)el.checked=true;
 });
}
document.addEventListener('click',function(e){
 var t=e.target;
 var tog=t.closest?t.closest('[data-toggle]'):null;
 if(tog){
  var id=tog.getAttribute('data-toggle'),b=$('body-'+id),sec=$('sec-'+id);
  b.hidden=!b.hidden;sec.classList.toggle('open',!b.hidden);
  tog.querySelector('.tw').textContent=b.hidden?'+':'\u2212';
  return;
 }
 var q=t.getAttribute&&t.getAttribute('data-quick');
 if(q){
  var s=sectionById(t.getAttribute('data-sec'));
  if(q==='nochange'){clearSection(s);setSecState(s.id,'nochange')}
  if(q==='normal'){applyNormal(s);setSecState(s.id,'normal')}
  if(q==='declined'){clearSection(s);setSecState(s.id,'declined')}
  if(q==='reset'){clearSection(s);setSecState(s.id,'')}
  return;
 }
 var c=t.getAttribute&&t.getAttribute('data-clear');
 if(c){document.querySelectorAll('#chips-'+c+' input').forEach(function(el){el.checked=false});
  var o=$(c+'_other');if(o)o.value='';refresh()}
});

/* ============ PREFILL ============ */
$('btnPrefill').addEventListener('click',function(){
 var raw=$('prefill').value.toLowerCase();
 if(!raw.trim()){$('prefillStatus').textContent='Nothing pasted yet.';return}
 var hits=0;
 ROOT.querySelectorAll('.chips input[data-t]').forEach(function(el){
  var lbl=el.parentElement.querySelector('span').textContent.toLowerCase();
  var key=lbl.split(',')[0].replace(/^(needs help |reports |uses |has a |takes |sees a )/,'').trim();
  if(key.length<4)return;
  if(raw.indexOf(key)>-1){el.checked=true;hits++}
 });
 $('prefillStatus').textContent=hits+' item'+(hits===1?'':'s')+' preselected. Confirm each with the patient before relying on it.';
 refresh();
});
$('btnClearPrefill').addEventListener('click',function(){$('prefill').value='';$('prefillStatus').textContent='';});

/* ============ BLOOD PRESSURE LOGIC ============ */
function bpBlock(){
 var o=bpOutcome();
 if(o==='obtained'&&v('bp'))
  return {ok:true,text:'Blood pressure '+v('bp')+', '+(v('bpSrc')||'source not recorded')+(v('bpDate')?', '+v('bpDate'):'')+'.',alert:''};
 if(o==='prior')
  return {ok:false,
   text:'No blood pressure could be obtained during this visit. Reason: '+(v('bpReason')||'patient has no home device')+'. Most recent value on record: '+(v('bp')||'none available')+', '+(v('bpSrc')||'source not recorded')+(v('bpDate')?', taken '+v('bpDate'):'')+'. This value was reviewed with the patient today and was not measured today. The measurement element is therefore not satisfied by a current reading and this visit is referred to the supervising physician as incomplete pending a decision.',
   alert:'No current blood pressure. Patient has no device. Most recent recorded value reviewed with the patient. The measurement element is a named requirement with no alternative, so the decision whether to bill, hold, or arrange a reading belongs to the practice.'};
 if(o==='declined')
  return {ok:false,
   text:'Blood pressure measurement was offered and the patient declined. Stated reason: '+(v('bpReason')||'not stated')+'. Most recent value on record: '+(v('bp')||'none available')+(v('bpDate')?', taken '+v('bpDate'):'')+'. Not measured today. Referred to the supervising physician as incomplete pending a decision.',
   alert:'Patient declined a blood pressure reading. Unlike advance care planning and the physical activity and nutrition assessment, the measurement element carries no discretion language, so a decline leaves a named element unfurnished. Decision to bill, hold, or rearrange belongs to the practice.'};
 return {ok:false,text:'',alert:''};
}
function renderBpAlert(){
 var b=bpBlock(),el=$('bpAlert');
 el.innerHTML=b.alert?'<div class="alertline">'+esc(b.alert)+'</div>':'';
}

/* ============ NOTE ============ */
function block(t,b){return b?(t.toUpperCase()+'\n'+b+'\n\n'):''}
function sectionText(s){
 var st=secState[s.id];
 if(st==='declined')return 'Offered and the patient declined. Documented as offered and declined at the patient\'s election.';
 var parts=[];
 if(st==='nochange')parts.push('Reviewed with the patient. No change reported since the last visit. Prior information carried forward and confirmed.');
 s.groups.forEach(function(g){
  var t=v(g.id);
  if(t)parts.push(g.t+': '+t+'.');
 });
 return parts.join('\n');
}
function buildNote(){
 var isInit=vtype()==='initial',code=isInit?'G0438':'G0439',mod=$('mod').value;
 var n=(isInit?'MEDICARE ANNUAL WELLNESS VISIT, FIRST':'MEDICARE ANNUAL WELLNESS VISIT, SUBSEQUENT')+'\n';
 n+='Supports HCPCS '+code+'. Elements furnished per 42 CFR 410.15. Preventive personalized prevention plan service. No physical examination, diagnosis, or treatment was performed by the nurse.\n\n';
 n+='Patient: '+(v('ptName')||'[name]')+'\nDate of birth: '+(fmtDate(v('ptDob'))||'[dob]')+'\nChart number: '+(v('mrn')||'[mrn]')+'\n';
 n+='Date of service: '+(fmtDate(v('dos'))||'[date]')+'\nModality: '+mod+(mod==='in person'?'':', patient located at '+(v('ptLocation')||'[location]'))+'\n';
 n+='Performed by: '+(v('nurse')||'[nurse]')+'\nSupervising physician: '+(v('physician')||'[physician]')+'\n';
 n+='Supervision: '+(v('supMethod')||'[method]')+'. The supervising physician was immediately available to provide assistance and direction throughout the service.\n';
 if(v('others'))n+='Others present: '+v('others')+'\n';
 if(v('eligNote'))n+='Eligibility: '+v('eligNote')+'\n';
 n+='\n'+block('Consent and expectations',v('consent')||'Not documented');
 var declined=[];
 SECTIONS.forEach(function(s){
  if(!isActive(s))return;
  if(s.id==='opioid'&&opioidGate()==='no'){
   n+=block(s.n+'  '+s.cite,'Chart reviewed. No current opioid prescription, so the opioid review elements do not apply.');
   return;
  }
  if(s.id==='measure'){
   var b=bpBlock(),m='';
   if(v('wt'))m+='Weight: '+v('wt')+'\n';
   if(v('waist'))m+='Waist circumference: '+v('waist')+'\n';
   if(isInit&&v('ht'))m+='Height: '+v('ht')+'\n';
   if(isInit&&v('bmi'))m+='Body mass index: '+v('bmi')+'\n';
   if(b.text)m+=b.text+'\n';
   if(v('wtChange'))m+='Weight change: '+v('wtChange')+'.\n';
   n+=block(s.n+'  '+s.cite,m);
   return;
  }
  if(s.id==='depression'){
   var d='',t=phqTotal();
   if(t!==null)d+='Two item screen administered. Item one '+$('phq1').value+', item two '+$('phq2').value+', total '+t+' of 6. Screen '+(t>=3?'POSITIVE':'negative')+'.\n';
   if(v('phq9'))d+='Nine item screen: '+v('phq9')+'\n';
   if(v('safetyItem'))d+='Self harm question: '+v('safetyItem')+'\n';
   var st=sectionText(s);if(st)d+=st;
   n+=block(s.n+'  '+s.cite,d);
   return;
  }
  if(s.id==='cognitive'){
   var c=sectionText(s);
   if(v('cogTool'))c+='\nStandardized instrument: '+v('cogTool')+(v('cogScore')?', score '+v('cogScore'):'')+'.';
   if(c)c+='\nElement furnished by direct observation with due consideration of patient and informant report. Result recorded for physician review. No interpretation was provided to the patient by the nurse.';
   n+=block(s.n+'  '+s.cite,c);
   return;
  }
  if(secState[s.id]==='declined')declined.push(s.n);
  var txt=sectionText(s);
  if(txt)n+=block(s.n+'  '+s.cite,txt);
 });
 if(declined.length)n+=block('Elements offered and declined',declined.join('; ')+'. Each was offered and the patient elected not to proceed.');
 n+='ATTESTATION\nAuthored by '+(v('nurse')||'[nurse]')+' under the direct supervision of '+(v('physician')||'[physician]')+'.\n';
 n+='Physician attestation: I was immediately available to provide assistance and direction throughout this service by the method documented above. I have reviewed the updated health risk assessment, the findings recorded, and the personalized prevention plan, and I agree with the plan as documented.\n\nPhysician signature: ______________________  Date: ____________\n';
 return n;
}

/* ============ CHECKLIST ============ */
function elementDone(s){
 if(s.id==='programs'||s.id==='esc')return null;
 if(s.id==='opioid'&&opioidGate()==='no')return true;
 if(s.id==='measure')return (v('wt')||v('waist'))&&bpBlock().ok;
 if(s.id==='depression')return phqTotal()!==null&&v('safetyItem');
 if(secState[s.id]==='nochange'||secState[s.id]==='declined')return true;
 return secHasContent(s);
}
function renderChecklist(){
 var ol=$('checklist');ol.innerHTML='';
 var req=0,ok=0;
 SECTIONS.forEach(function(s){
  if(!isActive(s))return;
  var d=elementDone(s);
  if(d===null)return;
  req++;if(d)ok++;
  var li=document.createElement('li');
  li.className=d?'done':'todo';
  li.innerHTML=esc(s.n)+' <span>'+esc(s.cite)+'</span>';
  ol.appendChild(li);
 });
 $('setLabel').textContent=(vtype()==='initial'?'First visit element set. ':'Subsequent visit element set. ')+ok+' of '+req+' complete.';
}
function renderStatuses(){
 SECTIONS.forEach(function(s){
  var el=$('st-'+s.id),sec=$('sec-'+s.id);
  if(!el)return;
  sec.hidden=!isActive(s);
  var st=secState[s.id],label='open',cls='';
  if(s.id==='measure'){var b=bpBlock();
   if(b.ok&&(v('wt')||v('waist'))){label='recorded';cls='ok'}
   else if(bpOutcome()){label='needs physician';cls='dec'}
  } else if(s.id==='opioid'&&opioidGate()==='no'){label='n/a';cls='ok'}
  else if(st==='declined'){label='declined';cls='dec'}
  else if(st==='nochange'){label='no change';cls='ok'}
  else if(st==='normal'){label='normal';cls='ok'}
  else if(secHasContent(s)){label='recorded';cls='ok'}
  el.textContent=label;el.className='st '+cls;
 });
}

/* ============ REVIEW LAYER ============ */
var RULES=[
 {id:'dyspnea',fields:['hxUpdate','hraFlags','providers','adl','socialNeeds'],kw:['short of breath','winded','oxygen'],
  finding:'Respiratory or exertional concern recorded',
  consider:'Heart failure, chronic obstructive pulmonary disease, anemia, deconditioning',
  codes:'I50.- heart failure by type, J44.- COPD, D64.9 anemia unspecified, R06.02 shortness of breath',
  needs:'Your own assessment. For heart failure document type and status. For COPD document supporting spirometry. R06.02 is a symptom code and should not stand in for an undiagnosed condition.'},
 {id:'oxygen',fields:['providers'],kw:['oxygen','cpap','nebulizer'],
  finding:'Home respiratory equipment recorded',
  consider:'Chronic respiratory failure, severe COPD, sleep apnea, heart failure with hypoxia',
  codes:'Z99.81 dependence on supplemental oxygen, J96.1- chronic respiratory failure, G47.33 obstructive sleep apnea',
  needs:'Status codes require the underlying condition documented and assessed. Chronic respiratory failure requires supporting saturation or blood gas evidence.'},
 {id:'mobility',fields:['providers','adl','fallDetail'],kw:['walker','cane','wheelchair','help bathing','help dressing','aide'],
  finding:'Mobility or personal care assistance recorded',
  consider:'Gait abnormality, mobility impairment, functional decline, or an underlying condition causing it',
  codes:'R26.- abnormalities of gait and mobility, Z74.09 other reduced mobility, Z99.3 dependence on wheelchair',
  needs:'These are function codes, not diagnoses. The useful step is documenting the condition causing the impairment.'},
 {id:'renal',fields:['providers','chronicList'],kw:['nephrologist','dialysis','kidney'],
  finding:'Kidney specialty care recorded',
  consider:'Chronic kidney disease by stage, or end stage renal disease',
  codes:'N18.1 through N18.6 by stage, Z99.2 dependence on dialysis',
  needs:'Stage must come from a current estimated glomerular filtration rate. Unspecified chronic kidney disease is a common audit finding.'},
 {id:'diabetes',fields:['meds','chronicList'],kw:['insulin','diabetes','glucose meter'],
  finding:'Diabetes treatment or monitoring recorded',
  consider:'Diabetes mellitus and whether chronic complications are present and documented',
  codes:'E11.- with the appropriate manifestation, Z79.4 long term insulin use',
  needs:'Your assessment of control and plan. Under the current risk model diabetes with and without chronic complications carry the same weight, so document a complication only where it is real.'},
 {id:'adherence',fields:['meds','socialNeeds','hraFlags'],kw:['skipping doses','running out','cost','manages the pills'],
  finding:'Medication access or adherence difficulty recorded',
  consider:'Medication nonadherence and social risk affecting treatment',
  codes:'Z91.12- intentional underdosing, Z91.13- unintentional underdosing, Z59.- economic circumstances',
  needs:'Clarify intentional versus unintentional. Strongest single indicator for care management enrollment.'},
 {id:'malnutrition',fields:['wtChange','hraFlags'],kw:['losing weight','looser','not eating','nutrition concern'],
  finding:'Weight loss or reduced intake recorded',
  consider:'Malnutrition, cachexia, or an underlying cause of unintentional weight loss',
  codes:'E44.- protein calorie malnutrition by degree, R63.4 abnormal weight loss, R63.0 anorexia',
  needs:'A known audit target requiring documented clinical criteria including intake, weight trend, and physical findings, plus a treatment plan. Do not code on patient report alone.'},
 {id:'mood',fields:['hraFlags','moodQuote','bhStatus'],kw:['low mood','loss of interest','lonely','feeling down','grief','counselor','anxiety'],
  finding:'Mood or behavioral health concern recorded',
  consider:'Major depressive disorder, adjustment disorder, grief reaction, anxiety, or a medical cause',
  codes:'F32.- single episode, F33.- recurrent, F43.2- adjustment disorder, F41.- anxiety',
  needs:'Your diagnostic assessment. A positive screening score is a screen, not a diagnosis, and coding from a screen alone is a documented audit failure.'},
 {id:'cognitive',fields:['cogObs','cogReport','meds','adl'],kw:['memory','repeat','missing appointments','word finding','disoriented','lost track','could not name','managing the pills'],
  finding:'Change in memory or thinking recorded',
  consider:'Mild cognitive impairment, dementia, delirium, depression presenting as cognitive change, medication effect',
  codes:'G31.84 mild cognitive impairment, F03.- unspecified dementia with severity, R41.3 other amnesia',
  needs:'A formal cognitive assessment and evaluation for reversible causes. Consider whether a separate cognitive assessment and care plan service is warranted, which is your work rather than the nurse\'s.'},
 {id:'falls',fields:['fallDetail','homeSafety','hraFlags','adl'],kw:['fall','unsteady','dizzy','passed out','balance'],
  finding:'Falls, unsteadiness, or presyncope recorded',
  consider:'Repeated falls, gait instability, orthostatic hypotension, syncope, medication effect',
  codes:'R29.6 repeated falls, W19.XXXA unspecified fall, I95.1 orthostatic hypotension, R55 syncope',
  needs:'Orthostatic vitals and a medication review. Orthostatic hypotension requires measured supine and standing pressures.'},
 {id:'substance',fields:['substance'],kw:['most days','six or more','current smoker','pack years','cannabis','not prescribed'],
  finding:'Substance use pattern recorded',
  consider:'Alcohol use disorder, nicotine dependence, or other substance use disorder',
  codes:'F10.- alcohol related, F17.2- nicotine dependence by product, Z87.891 personal history of nicotine dependence',
  needs:'Quantity alone does not establish a disorder. Pack year history determines lung cancer screening eligibility, which is worth closing regardless of coding.'},
 {id:'social',fields:['socialNeeds','hraFlags'],kw:['lives alone','isolated','no transportation','afford','housing','utilities','safe at home'],
  finding:'Social risk or access barrier recorded',
  consider:'Circumstances affecting the ability to complete the plan written today',
  codes:'Z60.2 problems related to living alone, Z59.82 transportation insecurity, Z59.4- food insecurity',
  needs:'These rarely change payment. They are recorded because they change what plan is realistic and because they support navigation and care management services.'},
 {id:'pain',fields:['opioid','chronicList'],kw:['opioid','chronic pain','pain severity'],
  finding:'Pain or opioid therapy recorded',
  consider:'Chronic pain with the underlying cause, and opioid therapy requiring the documented review elements',
  codes:'G89.2- chronic pain, the site specific condition, Z79.891 long term opioid use',
  needs:'The wellness visit requires documented risk factors, current severity, treatment plan, and non-opioid options wherever an opioid prescription is current.'}
];
function sentencesFrom(t){return t.split(/(?<=[.!?])\s+|\n+/).map(function(s){return s.trim()}).filter(Boolean)}
function findEvidence(fields,kw){
 var hits=[];
 fields.forEach(function(f){
  var t=v(f);if(!t)return;
  sentencesFrom(t).forEach(function(s){var low=s.toLowerCase();
   for(var i=0;i<kw.length;i++){if(low.indexOf(kw[i])>-1){hits.push(s);return}}});
 });
 return hits}
function anyKw(f,k){return findEvidence(f,k).length>0}
function noneWord(id){var t=v(id).toLowerCase();return !t||t.indexOf('none')===0||t.indexOf('no ')===0}

var PROGRAMS=[
 {name:'Advanced primary care management',test:function(){return chronicCount()>=1},
  why:function(){return chronicCount()+' condition'+(chronicCount()===1?'':'s')+' recorded.'},
  what:'Monthly care coordination, 24 hour access to a care team member, an electronic care plan, and population management, tiered by condition count and dual eligible status.',
  needs:'Documented consent, an initiating visit where required, and the full element set delivered. Not billable in the same month as chronic care management, principal care management, or transitional care management for the same patient.'},
 {name:'Chronic care management',test:function(){return chronicCount()>=2},
  why:function(){return 'Two or more chronic conditions recorded.'},
  what:'Monthly clinical staff time for coordination between visits with a comprehensive care plan, counted by time.',
  needs:'Consent, a care plan available to the team, documented staff time. Choose this or advanced primary care management in a given month, not both.'},
 {name:'Transitional care management',test:function(){return !noneWord('recentHosp')},
  why:function(){return 'A recent facility discharge was recorded.'},
  what:'A time limited service after discharge from inpatient, observation, partial hospitalization, or a skilled nursing facility.',
  needs:'Verify discharge type and date, because emergency department discharges do not qualify. The contact and visit windows are strict, so route today.'},
 {name:'Remote physiologic monitoring',test:function(){return anyKw(['monitorWilling'],['willing','has a home','uses the device'])||anyKw(['chronicList'],['blood pressure','diabetes','heart failure'])||bpOutcome()==='prior'},
  why:function(){return bpOutcome()==='prior'?'No blood pressure device at home, and a monitorable condition or willingness was recorded.':'A monitorable condition, an existing device, or willingness was recorded.'},
  what:'Device supply and monitoring of physiologic data between visits, with treatment management time.',
  needs:'A qualifying device, consent, an established relationship, and a documented clinical reason the data will change management. This also solves the missing blood pressure problem for future visits, which is a clinical reason rather than a billing one.'},
 {name:'Cognitive assessment and care plan',test:function(){return v('cogTool')||anyKw(['cogReport','cogObs'],['memory','repeat','disorient','word finding'])},
  why:function(){return 'Cognitive screening was performed or a change was recorded.'},
  what:'A comprehensive evaluation of cognition with a written care plan covering function, safety, caregiver needs, medication reconciliation, and advance planning.',
  needs:'Physician or advanced practitioner work requiring a separate visit with its own elements. A positive screen is the trigger, not the service.'},
 {name:'Behavioral health integration or collaborative care',test:function(){var t=phqTotal();return (t!==null&&t>=3)||!noneWord('bhStatus')||anyKw(['hraFlags'],['low mood','loneliness'])},
  why:function(){return 'A mood concern or behavioral health need was recorded.'},
  what:'Monthly behavioral health care management inside primary care, either the general integration model or the collaborative care model with a psychiatric consultant.',
  needs:'Consent, a designated behavioral health care manager, and validated rating scale tracking. The collaborative model requires the psychiatric consultant relationship in place first.'},
 {name:'Caregiver training services',test:function(){return !noneWord('caregiver')},
  why:function(){return 'A caregiver is involved in daily care.'},
  what:'Training furnished to a caregiver, without the patient present, on the techniques needed to support the patient at home.',
  needs:'A treatment plan identifying what the caregiver needs to learn, patient consent to train them, and documentation of the training. Commonly overlooked and often what keeps the patient at home.'},
 {name:'Community health integration or principal illness navigation',test:function(){return !noneWord('socialNeeds')},
  why:function(){return 'An unmet social need or access barrier was recorded.'},
  what:'Monthly services addressing upstream drivers that are interfering with the diagnosis or treatment of a medical problem, furnished by auxiliary personnel including community health workers or navigators.',
  needs:'An initiating visit, which the wellness visit can serve as, plus consent and documentation linking the specific barrier to the medical problem it obstructs. That link is what makes this billable rather than merely kind.'},
 {name:'Physical activity and nutrition risk assessment',test:function(){return anyKw(['hraFlags','wtChange'],['physical inactivity','nutrition','losing weight','not eating'])},
  why:function(){return 'A known or suspected physical activity or nutrition need was recorded.'},
  what:'A standardized, evidence based assessment of physical activity and nutrition, 5 to 15 minutes, not more often than every six months. This replaced the former social determinants assessment under the same code from 1 January 2026.',
  needs:'Not a screening for every patient. There must be a known or suspected need, the results must be used to adjust the treatment plan, and follow up is required. No patient cost sharing when furnished with the wellness visit.'},
 {name:'Advance care planning',test:function(){return true},
  why:function(){return 'Appropriate to offer at every wellness visit.'},
  what:'A voluntary discussion of goals of care and advance directives, furnishable on the same day as the wellness visit.',
  needs:'Voluntary, and the patient may decline. Document the discussion, whether forms were completed, and total time. Cost sharing waived when furnished with the wellness visit by the same provider on the same day.'},
 {name:'Screening and immunization gap closure',test:function(){return !!v('schedule')},
  why:function(){return 'Screening and immunization status was recorded.'},
  what:'Ordering what the patient is due for, which is part of the prevention plan regardless of any program.',
  needs:'Pay particular attention to lung cancer screening eligibility, which depends on pack year history, and to dilated eye examination in patients with diabetes.'},
 {name:'Visit complexity add-on, if a problem visit occurs today',test:function(){return !noneWord('newSymptom')},
  why:function(){return 'A new symptom or concern was raised during the visit.'},
  what:'An add-on recognising longitudinal complex primary care. It attaches to a separately identifiable office or outpatient evaluation and management service, not to the wellness visit code.',
  needs:'Payable alongside a wellness visit only when a separately identifiable problem visit is documented and reported with modifier 25 by the same practitioner on the same day. Not payable in rural health clinics or health centers.'}
];

function renderAlerts(){
 var out=$('alertsOut');out.innerHTML='';
 var a=[];
 var b=bpBlock();
 if(b.alert)a.push('Blood pressure: '+b.alert);
 if(v('safetyItem').indexOf('POSITIVE')===0)a.push('Depression screen self harm item positive. Escalation protocol was activated during the visit.');
 if(!noneWord('escImmediate'))a.push('Immediate escalation occurred during the visit: '+v('escImmediate'));
 if(!noneWord('newSymptom'))a.push('New symptom raised during the visit: '+v('newSymptom'));
 a.forEach(function(x){var d=document.createElement('div');d.className='alertline';d.textContent=x;out.appendChild(d)});
}
function runFlags(){
 renderAlerts();
 var out=$('flagsOut');out.innerHTML='';
 var any=false,ctx=$('payer').value;
 var hdr=document.createElement('p');hdr.className='sub';
 hdr.textContent=ctx==='ffs'
  ?'Payer context: traditional Medicare. Diagnoses do not change payment for this visit. This list exists so conditions are identified and treated.'
  :(ctx==='ma'
   ?'Payer context: Medicare Advantage. A registered nurse is not an acceptable provider type for risk adjustment, so nothing here supports a code until you assess the patient yourself and document your evaluation and plan.'
   :'Payer context: value based contract. Conditions must be assessed and documented by you. Quality gaps matter as much as diagnoses.');
 out.appendChild(hdr);
 RULES.forEach(function(r){
  var ev=findEvidence(r.fields,r.kw);
  if(!ev.length)return;any=true;
  var d=document.createElement('div');d.className='flag';
  d.innerHTML='<div class="fh">'+esc(r.finding)+'</div><div class="lbl">What was recorded</div>'+
   ev.slice(0,3).map(function(e){return '<div class="ev">'+esc(e)+'</div>'}).join('')+
   '<div class="lbl">Consider evaluating for</div><div class="body">'+esc(r.consider)+'</div>'+
   '<div class="lbl">Candidate codes if your assessment supports them</div><div class="codes">'+esc(r.codes)+'</div>'+
   '<div class="lbl">What your documentation needs</div><div class="body">'+esc(r.needs)+'</div>'+
   '<div class="decide">'+
    '<label><input type="radio" name="dec-'+r.id+'"><span>Assessed today</span></label>'+
    '<label><input type="radio" name="dec-'+r.id+'"><span>Not supported</span></label>'+
    '<label><input type="radio" name="dec-'+r.id+'"><span>Defer</span></label></div>';
  out.appendChild(d);
 });
 if(!any){var p=document.createElement('p');p.className='empty';
  p.textContent='No findings matched what was recorded.';out.appendChild(p)}
 runCorrob();runPrograms();
}
function runCorrob(){
 var out=$('corrobOut');out.innerHTML='';
 var list=v('problemList').split('\n').map(function(s){return s.trim()}).filter(Boolean);
 if(!list.length){out.innerHTML='<p class="empty">No problem list entered.</p>';return}
 var all=SECTIONS.reduce(function(acc,s){return acc.concat(s.groups.map(function(g){return v(g.id)}))},[]).join(' ').toLowerCase();
 list.forEach(function(cond){
  var tokens=cond.toLowerCase().split(/\s+/).filter(function(w){return w.length>3});
  var supported=tokens.some(function(w){return all.indexOf(w)>-1});
  var d=document.createElement('div');d.className='flag';
  d.innerHTML='<div class="fh">'+esc(cond)+'</div><div class="lbl">Corroborated today</div><div class="body">'+
   (supported?'Yes. Something recorded today relates to it. Confirm on your own assessment before documenting it as active.'
    :'No. Nothing recorded today referred to this condition. Reassess whether it is still active, resolved, or was recorded in error.')+'</div>';
  out.appendChild(d);
 });
}
function runPrograms(){
 var out=$('programsOut');out.innerHTML='';var any=false;
 PROGRAMS.forEach(function(p){
  var ok=false;try{ok=!!p.test()}catch(e){}
  if(!ok)return;any=true;
  var d=document.createElement('div');d.className='flag';
  d.innerHTML='<div class="fh">'+esc(p.name)+'</div>'+
   '<div class="lbl">Why it appeared</div><div class="body">'+esc(p.why())+'</div>'+
   '<div class="lbl">What the program is</div><div class="body">'+esc(p.what)+'</div>'+
   '<div class="lbl">Required before it can be furnished</div><div class="body">'+esc(p.needs)+'</div>'+
   '<div class="decide">'+
    '<label><input type="radio" name="prog-'+p.name.replace(/\W/g,'')+'"><span>Offer to patient</span></label>'+
    '<label><input type="radio" name="prog-'+p.name.replace(/\W/g,'')+'"><span>Not appropriate</span></label>'+
    '<label><input type="radio" name="prog-'+p.name.replace(/\W/g,'')+'"><span>Revisit later</span></label></div>';
  out.appendChild(d);
 });
 if(!any){var e=document.createElement('p');e.className='empty';e.textContent='No program criteria met.';out.appendChild(e)}
}
function decisionOf(f){var d=f.querySelector('.decide input:checked');return d?d.parentElement.querySelector('span').textContent:'No decision recorded'}
function flagsAsText(){
 var t='PHYSICIAN REVIEW SHEET\nWork product for the supervising physician. Not part of the visit note. Generated from information documented in the wellness visit note. Nothing here is a diagnosis and nothing has been coded.\n\n';
 t+='Patient: '+(v('ptName')||'[name]')+'   Chart: '+(v('mrn')||'[mrn]')+'   Date of service: '+(fmtDate(v('dos'))||'[date]')+'\n';
 t+='Prepared by: '+(v('nurse')||'[nurse]')+'   Supervising physician: '+(v('physician')||'[physician]')+'\n\n';
 var al=[];document.querySelectorAll('#alertsOut .alertline').forEach(function(x){al.push(x.textContent)});
 if(al.length)t+='NEEDS A DECISION FROM YOU\n'+al.map(function(x){return '  '+x}).join('\n')+'\n\n';
 t+='FINDINGS FOR YOUR ASSESSMENT\n\n';
 document.querySelectorAll('#flagsOut .flag').forEach(function(f){
  t+=f.querySelector('.fh').textContent+'\n';
  f.querySelectorAll('.ev').forEach(function(e){t+='  Recorded: '+e.textContent+'\n'});
  var b=f.querySelectorAll('.body'),c=f.querySelector('.codes');
  if(b[0])t+='  Consider: '+b[0].textContent+'\n';
  if(c)t+='  Candidate codes: '+c.textContent+'\n';
  if(b[1])t+='  Documentation needed: '+b[1].textContent+'\n';
  t+='  Physician decision: '+decisionOf(f)+'\n\n';
 });
 t+='PROBLEM LIST CORROBORATION\n';
 document.querySelectorAll('#corrobOut .flag').forEach(function(f){
  t+=f.querySelector('.fh').textContent+': '+f.querySelector('.body').textContent+'\n'});
 t+='\nPROGRAM CANDIDACY\n\n';
 document.querySelectorAll('#programsOut .flag').forEach(function(f){
  var b=f.querySelectorAll('.body');
  t+=f.querySelector('.fh').textContent+'\n';
  if(b[0])t+='  Why: '+b[0].textContent+'\n';
  if(b[2])t+='  Required first: '+b[2].textContent+'\n';
  t+='  Physician decision: '+decisionOf(f)+'\n\n';
 });
 return t}
function decisionsAsText(){
 var t='PHYSICIAN DECISIONS, '+(fmtDate(v('dos'))||'[date]')+'\n';
 t+='Reviewed the nurse-documented wellness visit findings for '+(v('ptName')||'[name]')+', chart '+(v('mrn')||'[mrn]')+'.\n\n';
 var n=0;
 document.querySelectorAll('#flagsOut .flag, #programsOut .flag').forEach(function(f){
  var d=f.querySelector('.decide input:checked');if(!d)return;n++;
  t+=n+'. '+f.querySelector('.fh').textContent+': '+d.parentElement.querySelector('span').textContent+'\n';
 });
 if(!n)t+='No decisions recorded yet.\n';
 var b=bpBlock();
 if(!b.ok&&bpOutcome())t+='\nBlood pressure element: decision required on whether to bill, hold the encounter open, or arrange a reading.\n';
 t+='\nItems marked as assessed were evaluated by me during a face to face encounter and are documented separately in my own note. Items marked not supported were considered and are not established.\n';
 return t}

/* ============ SESSION ============ */
var noteEl=$('noteOut'),userEdited=false;
noteEl.addEventListener('input',function(){userEdited=true});
function hasData(){
 if(v('ptName')||v('mrn')||v('prefill')||v('problemList'))return true;
 return SECTIONS.some(function(s){return secHasContent(s)});
}
function wipeAll(silent){
 ROOT.querySelectorAll('input[type=text],input[type=date],textarea').forEach(function(el){
  if(el.id==='noteOut'||el.hasAttribute('data-profile'))return;el.value=''});
 ROOT.querySelectorAll('select').forEach(function(el){
  if(!el.hasAttribute('data-profile')&&['vtype','mod','payer'].indexOf(el.id)<0)el.selectedIndex=0});
 ROOT.querySelectorAll('input[type=checkbox],input[type=radio]').forEach(function(el){el.checked=false});
 var og=ROOT.querySelector('input[name=opioidGate][value=no]');if(og)og.checked=true;
 secState={};userEdited=false;noteEl.value='';
 $('flagsOut').innerHTML='<p class="empty">Complete the worksheet, then generate.</p>';
 $('alertsOut').innerHTML='';
 $('corrobOut').innerHTML='<p class="empty">Enter the problem list, then generate.</p>';
 $('programsOut').innerHTML='<p class="empty">Complete the worksheet, then generate.</p>';
 $('prefillStatus').textContent='';
 refresh();
 if(!silent)$('sessStatus').textContent='Wiped at '+new Date().toLocaleTimeString()+'.';
}
var idleTimer=null;
function resetIdle(){if(idleTimer)clearTimeout(idleTimer);
 idleTimer=setTimeout(function(){if(hasData()){wipeAll(true);
  $('sessStatus').textContent='Wiped automatically after 20 minutes of inactivity.'}},20*60*1000)}
ROOT.querySelectorAll('input,textarea,select').forEach(function(el){
 el.setAttribute('autocomplete','off');el.setAttribute('autocapitalize','off');
 if(el.tagName==='TEXTAREA'||el.type==='text')el.setAttribute('spellcheck','false')});

/* ============ PROFILE ============ */
var PKEY='awv_operator_profile_v4';
function profileFields(){return Array.prototype.slice.call(ROOT.querySelectorAll('[data-profile]'))}
$('btnSaveProfile').addEventListener('click',function(){
 var o={};profileFields().forEach(function(el){o[el.id]=el.value});
 try{localStorage.setItem(PKEY,JSON.stringify(o));
  $('profileStatus').textContent='Saved on this device at '+new Date().toLocaleTimeString()+'. Operator details only.'}
 catch(e){$('profileStatus').textContent='This browser will not store data for a file opened straight from disk. Serve it from a local web server and saving will work.'}
 refresh();
});
$('btnForgetProfile').addEventListener('click',function(){
 try{localStorage.removeItem(PKEY)}catch(e){}
 profileFields().forEach(function(el){el.value=''});
 $('profileStatus').textContent='Saved details removed from this device.';refresh();
});
(function(){try{var raw=localStorage.getItem(PKEY);
 if(!raw){$('profileStatus').textContent='Nothing saved yet on this device.';return}
 var o=JSON.parse(raw);profileFields().forEach(function(el){if(o[el.id]!==undefined)el.value=o[el.id]});
 $('profileStatus').textContent='Loaded saved operator details.'}
 catch(e){$('profileStatus').textContent='No stored details available in this browser.'}})();

$('btnToday').addEventListener('click',function(){
 var d=new Date();
 $('dos').value=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
 refresh();
});

/* ============ REFRESH ============ */
function refresh(){
 var isInit=vtype()==='initial';
 $('htbmi').innerHTML=isInit
  ?'<label class="fl" for="ht">Height</label><input type="text" id="ht">'
  :'';
 renderStatuses();renderChecklist();renderBpAlert();
 var t=phqTotal(),ps=$('phqScore');
 if(ps)ps.textContent=t===null?'Two item total: not yet scored'
  :('Two item total: '+t+' of 6, '+(t>=3?'positive, administer the nine item screen':'negative'));
 if(!userEdited)noteEl.value=buildNote();
 $('sessStatus').textContent=hasData()?'Patient information is on screen. Wipe before you step away.':'No patient information entered.';
}
document.addEventListener('input',function(){resetIdle();refresh()});
document.addEventListener('change',function(){resetIdle();refresh()});
ROOT.querySelectorAll('.tabs button').forEach(function(b){
 b.addEventListener('click',function(){
  ROOT.querySelectorAll('.tabs button').forEach(function(x){x.setAttribute('aria-selected','false')});
  b.setAttribute('aria-selected','true');
  ['nurse','review','why'].forEach(function(t){$('tab-'+t).hidden=(t!==b.dataset.tab)});
 });
});
window.addEventListener('beforeunload',function(e){if(hasData()){e.preventDefault();e.returnValue=''}});
$('btnEndSession').addEventListener('click',function(){
 if(!hasData()||window.confirm('Wipe everything on screen? Saved operator details are kept.'))wipeAll(false)});
$('btnRunFlags').addEventListener('click',runFlags);
$('btnCopyFlags').addEventListener('click',function(){
 var t=flagsAsText();
 if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(function(){
  $('btnCopyFlags').textContent='Copied';setTimeout(function(){$('btnCopyFlags').textContent='Copy review sheet'},1500)},function(){})});
$('btnCopyDecisions').addEventListener('click',function(){
 var t=decisionsAsText();
 if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(function(){
  $('btnCopyDecisions').textContent='Copied';setTimeout(function(){$('btnCopyDecisions').textContent='Copy decisions only'},1500)},function(){})});
$('btnCopy').addEventListener('click',function(){
 noteEl.select();noteEl.setSelectionRange(0,999999);
 try{document.execCommand('copy')}catch(e){}
 if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(noteEl.value).then(function(){
  $('btnCopy').textContent='Copied';setTimeout(function(){$('btnCopy').textContent='Copy note'},1500)},function(){})});
$('btnWord').addEventListener('click',function(){
 var body=noteEl.value.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
 var html='<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">'+
  '<head><meta charset="utf-8"><title>Annual Wellness Visit Note</title></head>'+
  '<body style="font-family:Calibri,Arial,sans-serif;font-size:11pt;line-height:1.4">'+body+'</body></html>';
 var blob=new Blob(['\ufeff',html],{type:'application/msword'}),url=URL.createObjectURL(blob),a=document.createElement('a');
 a.href=url;a.download='awv-note-'+((v('ptName')||'patient').replace(/[^a-z0-9]+/gi,'-').toLowerCase())+'.doc';
 document.body.appendChild(a);a.click();document.body.removeChild(a);
 setTimeout(function(){URL.revokeObjectURL(url)},2000)});
$('btnPrint').addEventListener('click',function(){window.print()});
resetIdle();refresh();
})();
