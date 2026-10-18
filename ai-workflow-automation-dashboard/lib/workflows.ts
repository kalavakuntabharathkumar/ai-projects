import type { Workflow } from './types';

const initial: Workflow[] = [
 { id:'wf-001', name:'Support ticket triage', description:'Classify new tickets and suggest the right queue.', status:'Active', owner:'Customer Operations', updatedAt:'2026-10-17', nodes:[{id:'n1',kind:'trigger',title:'New ticket',config:{source:'Support inbox'}},{id:'n2',kind:'llm',title:'Classify ticket',config:{model:'Claude',promptVersion:'v2'}},{id:'n3',kind:'condition',title:'Urgent?',config:{field:'priority',operator:'equals',value:'urgent'}},{id:'n4',kind:'action',title:'Assign queue',config:{destination:'Support team'}}] },
 { id:'wf-002', name:'Weekly feedback digest', description:'Summarize product feedback for the product team.', status:'Draft', owner:'Product Operations', updatedAt:'2026-10-16', nodes:[{id:'n1',kind:'trigger',title:'Weekly schedule',config:{schedule:'Monday 09:00'}},{id:'n2',kind:'llm',title:'Summarize feedback',config:{model:'Configured provider',maxItems:'100'}},{id:'n3',kind:'action',title:'Create digest',config:{destination:'Draft report'}}] },
 { id:'wf-003', name:'Invoice exception review', description:'Flag invoice records that need a human review.', status:'Paused', owner:'Finance Operations', updatedAt:'2026-10-12', nodes:[{id:'n1',kind:'trigger',title:'Invoice uploaded',config:{source:'Finance folder'}},{id:'n2',kind:'condition',title:'Missing fields?',config:{field:'requiredFields',operator:'containsMissing'}},{id:'n3',kind:'action',title:'Create review task',config:{destination:'Finance queue'}}] }
];
let workflows = initial.map(w => ({...w, nodes:w.nodes.map(n=>({...n,config:{...n.config}}))}));
export function listWorkflows(): Workflow[] { return workflows.map(w=>({...w,nodes:w.nodes.map(n=>({...n,config:{...n.config}}))})); }
export function getWorkflow(id: string): Workflow | undefined { return listWorkflows().find(w=>w.id===id); }
export function saveWorkflow(workflow: Workflow): Workflow {
 const clean = {...workflow, name:workflow.name.trim(), nodes:workflow.nodes.map(n=>({...n,config:{...n.config}}))};
 if (!clean.name) throw new Error('Workflow name is required');
 const index=workflows.findIndex(w=>w.id===clean.id);
 if(index<0) workflows=[clean,...workflows]; else workflows=workflows.map(w=>w.id===clean.id?clean:w);
 return clean;
}
export function deleteWorkflow(id: string): void { workflows=workflows.filter(w=>w.id!==id); }
export function resetWorkflowsForTests(): void { workflows=initial.map(w=>({...w,nodes:w.nodes.map(n=>({...n,config:{...n.config}}))})); }
