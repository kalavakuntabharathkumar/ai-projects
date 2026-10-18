import {NextResponse} from 'next/server';
import {listWorkflows,saveWorkflow} from '../../../lib/workflows';
import type {Workflow} from '../../../lib/types';
export async function GET(){return NextResponse.json({workflows:listWorkflows()});}
export async function POST(request:Request){try{const input=await request.json() as Workflow;if(!input||!input.name||!Array.isArray(input.nodes))return NextResponse.json({error:'name and nodes are required'},{status:400});const workflow=saveWorkflow(input);return NextResponse.json({workflow},{status:201});}catch(error){return NextResponse.json({error:error instanceof Error?error.message:'Invalid workflow'},{status:400});}}
