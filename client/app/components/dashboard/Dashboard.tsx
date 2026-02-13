'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface Project {
    id: string;
    title: string;
    thumbnailUrl: string | null;
    lastEdited: string;
    createdAt: string;
}

export function Dashboard() {
    const [projects, setProjects] = useState<Project[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();

    useEffect(() => {
        fetchProjects();
    }, []);

    const fetchProjects = async () => {
        try {
            setIsLoading(true);
            setError(null);
            const response = await fetch('http://127.0.0.1:8080/api/projects', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
                throw new Error(errorData.error || `Server error: ${response.status}`);
            }
            
            const data = await response.json();
            setProjects(data.projects || []);
        } catch (err) {
            console.error('Error fetching projects:', err);
            if (err instanceof TypeError && err.message.includes('fetch')) {
                setError('Unable to connect to server. Please make sure the backend server is running on port 8080.');
            } else {
                setError(err instanceof Error ? err.message : 'Failed to load projects');
            }
        } finally {
            setIsLoading(false);
        }
    };

    const formatDate = (dateString: string) => {
        if (!dateString) return 'Unknown';
        try {
            const date = new Date(dateString);
            const now = new Date();
            const diffMs = now.getTime() - date.getTime();
            const diffMins = Math.floor(diffMs / 60000);
            const diffHours = Math.floor(diffMs / 3600000);
            const diffDays = Math.floor(diffMs / 86400000);

            if (diffMins < 1) return 'Just now';
            if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
            if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
            if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
            
            return date.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric', 
                year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined 
            });
        } catch {
            return 'Unknown';
        }
    };

    const handleProjectClick = (projectId: string) => {
        router.push(`/editor/${projectId}`);
    };

    return (
        <div className="bg-[#0a0a0a] min-h-screen flex flex-col">
            {/* Header */}
            <header className="border-b border-[rgba(38,38,38,0.4)] h-[69px] flex items-center justify-between px-6">
                <div className="flex items-center gap-2">
                    <Link
                        href="/"
                        className="flex items-center gap-2"
                    >
                        <div
                            className="w-8 h-8 rounded-[10px] flex items-center justify-center flex-shrink-0"
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
                    </Link>
                </div>
                <nav className="flex items-center gap-4 sm:gap-6">
                    <Link
                        href="/dashboard"
                        className="px-3 sm:px-4 py-2 text-[#fafafa] text-sm hover:opacity-80 transition-opacity"
                    >
                        Dashboard
                    </Link>
                    <Link
                        href="/create"
                        className="px-3 sm:px-4 py-2 bg-[#fafafa] text-[#171717] text-sm rounded-lg hover:opacity-90 transition-opacity"
                    >
                        Create Video
                    </Link>
                </nav>
            </header>

            {/* Main Content */}
            <main className="flex-1 pt-8 pb-12 px-4 sm:px-6 lg:px-12">
                <div className="max-w-7xl mx-auto">
                    {/* Page Title */}
                    <div className="mb-8">
                        <h2 className="text-3xl sm:text-4xl font-bold text-[#fafafa] mb-2">
                            My Projects
                        </h2>
                        <p className="text-[#a1a1a1] text-sm sm:text-base">
                            Manage and edit your video projects
                        </p>
                    </div>

                    {/* Loading State */}
                    {isLoading && (
                        <div className="flex items-center justify-center py-20">
                            <div className="flex flex-col items-center gap-4">
                                <svg className="animate-spin h-8 w-8 text-[#7f22fe]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                <p className="text-[#a1a1a1] text-sm">Loading projects...</p>
                            </div>
                        </div>
                    )}

                    {/* Error State */}
                    {error && !isLoading && (
                        <div className="bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg text-sm mb-6">
                            {error}
                        </div>
                    )}

                    {/* Empty State */}
                    {!isLoading && !error && projects.length === 0 && (
                        <div className="flex flex-col items-center justify-center py-20 text-center">
                            <div className="bg-[#262626] border border-[rgba(38,38,38,0.4)] rounded-[10px] w-16 h-16 flex items-center justify-center mb-4">
                                <img alt="Video icon" className="w-8 h-8" src={"/icons/imageIcon.svg"} loading="lazy" />
                            </div>
                            <h3 className="text-[#fafafa] text-xl font-semibold mb-2">No projects yet</h3>
                            <p className="text-[#a1a1a1] text-sm mb-6 max-w-md">
                                Create your first video project to get started
                            </p>
                            <Link
                                href="/create"
                                className="bg-[#7f22fe] text-white px-6 py-2 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity"
                            >
                                Create New Video
                            </Link>
                        </div>
                    )}

                    {/* Projects Grid */}
                    {!isLoading && !error && projects.length > 0 && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
                            {projects.map((project) => (
                                <div
                                    key={project.id}
                                    onClick={() => handleProjectClick(project.id)}
                                    className="bg-[rgba(38,38,38,0.3)] border border-[rgba(38,38,38,0.4)] rounded-lg overflow-hidden cursor-pointer hover:border-[rgba(142,81,255,0.4)] transition-all hover:shadow-lg hover:shadow-[rgba(142,81,255,0.1)] group"
                                >
                                    {/* Thumbnail */}
                                    <div className="relative w-full aspect-video bg-[#262626] overflow-hidden">
                                        {project.thumbnailUrl ? (
                                            <img
                                                src={`http://127.0.0.1:8080${project.thumbnailUrl}`}
                                                alt={project.title}
                                                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                                                onError={(e) => {
                                                    // Fallback to placeholder if image fails to load
                                                    const target = e.target as HTMLImageElement;
                                                    target.style.display = 'none';
                                                    const placeholder = target.parentElement?.querySelector('.thumbnail-placeholder') as HTMLElement;
                                                    if (placeholder) {
                                                        placeholder.style.display = 'flex';
                                                    }
                                                }}
                                            />
                                        ) : null}
                                        <div 
                                            className={`thumbnail-placeholder absolute inset-0 flex items-center justify-center ${project.thumbnailUrl ? 'hidden' : 'flex'}`}
                                        >
                                            <div className="bg-[rgba(38,38,38,0.5)] rounded-lg w-12 h-12 flex items-center justify-center">
                                                <img alt="Video icon" className="w-6 h-6 opacity-50" src={"/icons/imageIcon.svg"} />
                                            </div>
                                        </div>
                                    </div>

                                    {/* Project Info */}
                                    <div className="p-4">
                                        <h3 className="text-[#fafafa] text-base font-semibold mb-2 line-clamp-2 group-hover:text-[#a684ff] transition-colors">
                                            {project.title}
                                        </h3>
                                        <p className="text-[#a1a1a1] text-xs">
                                            Last edited {formatDate(project.lastEdited)}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}
