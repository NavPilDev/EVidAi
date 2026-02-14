'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface Project {
    id: string;
    title: string;
    description: string;
    thumbnailUrl: string | null;
    videoUrl: string | null;
    createdAt: string;
    lastEdited: string;
    audioFile: {
        filename: string;
        path: string;
        size: number;
    };
    referenceImages: Array<{
        filename: string;
        path: string;
    }>;
    storyboard: Record<string, any>;
    agentHistory: any[];
}

interface EditorProps {
    projectId: string;
}

export function Editor({ projectId }: EditorProps) {
    const [project, setProject] = useState<Project | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();

    useEffect(() => {
        fetchProject();
    }, [projectId]);

    const fetchProject = async () => {
        try {
            setIsLoading(true);
            setError(null);
            const response = await fetch(`http://127.0.0.1:8000/api/projects/${projectId}`);
            
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Project not found');
                }
                throw new Error('Failed to fetch project');
            }
            
            const data = await response.json();
            setProject(data);
        } catch (err) {
            console.error('Error fetching project:', err);
            setError(err instanceof Error ? err.message : 'Failed to load project');
        } finally {
            setIsLoading(false);
        }
    };

    const formatDate = (dateString: string) => {
        if (!dateString) return 'Unknown';
        try {
            const date = new Date(dateString);
            return date.toLocaleString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric',
                hour: 'numeric',
                minute: '2-digit',
            });
        } catch {
            return 'Unknown';
        }
    };

    return (
        <div className="bg-[#0a0a0a] min-h-screen flex flex-col">
            {/* Header */}
            <header className="bg-[rgba(10,10,10,0.8)] border-b border-[rgba(38,38,38,0.4)] h-[65px] flex items-center justify-between px-6">
                <div className="flex items-center gap-4">
                    <Link
                        href="/dashboard"
                        className="flex items-center gap-2 px-2 py-2 text-[#fafafa] text-sm hover:opacity-80 transition-opacity"
                    >
                        <img alt="Back arrow" className="w-4 h-4" src={"/icons/backArrowIcon.svg"} />
                        <span>Back to Dashboard</span>
                    </Link>
                    <div className="flex items-center gap-2">
                        <div
                            className="w-8 h-8 rounded-[10px] flex items-center justify-center"
                            style={{ backgroundImage: "linear-gradient(135deg, rgb(142, 81, 255) 0%, rgb(152, 16, 250) 100%)" }}
                        >
                            <img
                                alt="EvidAi logo icon"
                                className="w-5 h-5"
                                src={"/icons/logoIcon.svg"}
                                loading="eager"
                            />
                        </div>
                        <h1 className="text-[#fafafa] text-xl font-bold">EvidAi</h1>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-1 flex items-start justify-center pt-16 sm:pt-[113px] pb-12 px-4 sm:px-12">
                <div className="max-w-[848px] w-full flex flex-col gap-6 sm:gap-8">
                    {/* Loading State */}
                    {isLoading && (
                        <div className="flex items-center justify-center py-20">
                            <div className="flex flex-col items-center gap-4">
                                <svg className="animate-spin h-8 w-8 text-[#7f22fe]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                <p className="text-[#a1a1a1] text-sm">Loading project...</p>
                            </div>
                        </div>
                    )}

                    {/* Error State */}
                    {error && !isLoading && (
                        <div className="bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg text-sm">
                            {error}
                            <div className="mt-4">
                                <Link
                                    href="/dashboard"
                                    className="text-red-400 hover:text-red-300 underline text-sm"
                                >
                                    Return to Dashboard
                                </Link>
                            </div>
                        </div>
                    )}

                    {/* Project Content */}
                    {project && !isLoading && (
                        <>
                            {/* Title Section */}
                            <div className="flex flex-col gap-2">
                                <h2 className="text-2xl sm:text-[30px] font-bold text-[#fafafa] leading-tight sm:leading-[36px]">
                                    {project.title}
                                </h2>
                                <p className="text-[#a1a1a1] text-sm sm:text-base leading-6">
                                    Project Editor - ID: {project.id}
                                </p>
                            </div>

                            {/* Project Info Card */}
                            <div className="bg-[rgba(38,38,38,0.3)] border border-[rgba(38,38,38,0.4)] rounded-lg p-6">
                                <h3 className="text-[#fafafa] text-lg font-semibold mb-4">Project Details</h3>
                                
                                <div className="space-y-4">
                                    {/* Description */}
                                    {project.description && (
                                        <div>
                                            <label className="text-[#a1a1a1] text-xs uppercase tracking-wide mb-1 block">Description</label>
                                            <p className="text-[#fafafa] text-sm">{project.description}</p>
                                        </div>
                                    )}

                                    {/* Metadata */}
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                        <div>
                                            <label className="text-[#a1a1a1] text-xs uppercase tracking-wide mb-1 block">Created</label>
                                            <p className="text-[#fafafa] text-sm">{formatDate(project.createdAt)}</p>
                                        </div>
                                        <div>
                                            <label className="text-[#a1a1a1] text-xs uppercase tracking-wide mb-1 block">Last Edited</label>
                                            <p className="text-[#fafafa] text-sm">{formatDate(project.lastEdited)}</p>
                                        </div>
                                    </div>

                                    {/* Audio File */}
                                    {project.audioFile && (
                                        <div>
                                            <label className="text-[#a1a1a1] text-xs uppercase tracking-wide mb-1 block">Audio File</label>
                                            <p className="text-[#fafafa] text-sm">{project.audioFile.filename}</p>
                                            <p className="text-[#a1a1a1] text-xs mt-1">
                                                {(project.audioFile.size / 1024 / 1024).toFixed(2)} MB
                                            </p>
                                        </div>
                                    )}

                                    {/* Reference Images */}
                                    {project.referenceImages && project.referenceImages.length > 0 && (
                                        <div>
                                            <label className="text-[#a1a1a1] text-xs uppercase tracking-wide mb-2 block">
                                                Reference Images ({project.referenceImages.length})
                                            </label>
                                            <div className="flex flex-wrap gap-2">
                                                {project.referenceImages.map((img, index) => (
                                                    <div key={index} className="text-[#fafafa] text-xs bg-[rgba(38,38,38,0.5)] px-2 py-1 rounded">
                                                        {img.filename}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Video Status */}
                                    <div>
                                        <label className="text-[#a1a1a1] text-xs uppercase tracking-wide mb-1 block">Video Status</label>
                                        {project.videoUrl ? (
                                            <p className="text-green-400 text-sm">Video generated</p>
                                        ) : (
                                            <p className="text-[#a1a1a1] text-sm">Video pending generation</p>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Placeholder for Editor */}
                            <div className="bg-[rgba(38,38,38,0.3)] border border-[rgba(38,38,38,0.4)] rounded-lg p-8 text-center">
                                <div className="bg-[#262626] border border-[rgba(38,38,38,0.4)] rounded-[10px] w-16 h-16 flex items-center justify-center mx-auto mb-4">
                                    <img alt="Edit icon" className="w-8 h-8 opacity-50" src={"/icons/imageIcon.svg"} />
                                </div>
                                <h3 className="text-[#fafafa] text-lg font-semibold mb-2">Editor Coming Soon</h3>
                                <p className="text-[#a1a1a1] text-sm max-w-md mx-auto">
                                    The video editor interface will be available here. You'll be able to edit storyboards, view agent history, and make changes to your project.
                                </p>
                            </div>
                        </>
                    )}
                </div>
            </main>
        </div>
    );
}
