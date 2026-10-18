import {beforeEach,describe,expect,it} from 'vitest';
import {deleteWorkflow,getWorkflow,listWorkflows,resetWorkflowsForTests,saveWorkflow} from '../lib/workflows';
import type {Workflow} from '../lib/types';
beforeEach(()=>resetWorkflowsForTests());
describe('workflow store',()=>{
 it('starts with sample workflows',()=>{expect(listWorkflows().length).toBe(3)});
 it('returns a workflow by id',()=>{expect(getWorkflow('wf-001')?.name).toBe('Support ticket triage')});
 it('updates an existing workflow',()=>{const w=getWorkflow('wf-001')!;saveWorkflow({...w,name:'Updated triage'});expect(getWorkflow('wf-001')?.name).toBe('Updated triage')});
 it('rejects a blank name',()=>{const w=getWorkflow('wf-001')!;expect(()=>saveWorkflow({...w,name:'  '})).toThrow('Workflow name is required')});
 it('deletes a workflow',()=>{deleteWorkflow('wf-002');expect(getWorkflow('wf-002')).toBeUndefined()});
 it('returns defensive copies of nested nodes',()=>{const w=getWorkflow('wf-001')!;w.nodes[0].title='mutated';expect(getWorkflow('wf-001')!.nodes[0].title).toBe('New ticket')});
});
