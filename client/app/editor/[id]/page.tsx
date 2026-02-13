import { Editor } from '../../components/editor/Editor';

interface EditorPageProps {
    params: Promise<{
        id: string;
    }>;
}

export default async function EditorPage({ params }: EditorPageProps) {
    const { id } = await params;
    return <Editor projectId={id} />;
}
