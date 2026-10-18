import Shell from '../../../components/Shell';
import WorkflowEditor from '../../../components/WorkflowEditor';
export default function EditWorkflow({params}:{params:{id:string}}){return <Shell><div className="topline"><div><div className="eyebrow">Builder</div><h1 className="section-title">Edit workflow</h1><p className="muted">Review the flow and update its configuration.</p></div></div><WorkflowEditor workflowId={params.id}/></Shell>}
