import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'FlowPilot | AI Workflow Studio', description: 'Build and manage internal AI workflows.' };
export default function RootLayout({ children }: Readonly<{children: React.ReactNode}>) { return <html lang="en"><body>{children}</body></html>; }
