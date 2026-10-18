export type NodeKind = 'trigger' | 'llm' | 'condition' | 'action';
export type WorkflowNode = { id: string; kind: NodeKind; title: string; config: Record<string, string> };
export type Workflow = { id: string; name: string; description: string; status: 'Draft' | 'Active' | 'Paused'; owner: string; updatedAt: string; nodes: WorkflowNode[] };
