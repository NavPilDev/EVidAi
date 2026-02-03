'use client';

import Link from 'next/link';

// Image assets from Figma
const imgIcon = "http://localhost:3845/assets/6acc779ab6187548c05b4616eef4d73831fec25b.svg";
const imgIcon1 = "http://localhost:3845/assets/19e7ad499e9fa2e2482aa1e20cef37513608b59f.svg";
const imgIcon2 = "http://localhost:3845/assets/09ca5779317bb0ed546c9b7dd32547c24812caad.svg";
const imgIcon3 = "http://localhost:3845/assets/5dea59bc18633054a3f122606d38f38964cc84a6.svg";
const imgIcon4 = "http://localhost:3845/assets/0149f672be16eae545bee52e6dc1fae9fe277190.svg";
const imgEllipse1 = "http://localhost:3845/assets/fa0ae84c1a202b2d01f29d25d10edbf6243615e5.svg";
const imgIcon5 = "http://localhost:3845/assets/23bd4482d14a3ed265ad50d1c96d224a381aa9c6.svg";

export function HomePage() {
    return (
        <div className="bg-[#0a0a0a] min-h-screen flex flex-col">
            {/* Header */}
            <header className="border-b border-[rgba(38,38,38,0.4)] h-[69px] flex items-center justify-between px-6">
                <div className="flex items-center gap-2">
                    <div
                        className="w-8 h-8 rounded-[10px] flex items-center justify-center flex-shrink-0"
                        style={{ backgroundImage: "linear-gradient(135deg, rgb(142, 81, 255) 0%, rgb(152, 16, 250) 100%)" }}
                    >
                        <img
                            alt="EvidAi logo icon"
                            className="w-5 h-5"
                            src={imgIcon5}
                            loading="eager"
                        />
                    </div>
                    <h1 className="text-[#fafafa] text-xl font-bold">EvidAi</h1>
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
            <main className="flex-1 flex items-center justify-center pt-[69px] pb-[69px] px-4 sm:px-6">
                <div className="max-w-[768px] w-full px-6 sm:px-12 relative">
                    {/* Decorative ellipse */}
                    <div className="hidden md:block absolute left-[117px] top-[-100px] w-[553px] h-[553px] opacity-20 pointer-events-none">
                        <img
                            alt=""
                            className="w-full h-full"
                            src={imgEllipse1}
                            loading="lazy"
                        />
                    </div>

                    {/* AI-Powered Badge */}
                    <div className="relative mb-8 flex justify-center">
                        <div className="bg-[rgba(142,81,255,0.1)] border border-[rgba(142,81,255,0.2)] rounded-full px-3 py-2 flex items-center gap-2">
                            <img alt="Sparkle icon" className="w-4 h-4" src={imgIcon} loading="lazy" />
                            <span className="text-[#a684ff] text-sm">AI-Powered Video Creation</span>
                        </div>
                    </div>

                    {/* Main Heading */}
                    <div className="text-center mb-6">
                        <h2 className="text-4xl sm:text-5xl md:text-[60px] font-bold leading-tight sm:leading-[60px] tracking-[-1.5px] text-[#fafafa] mb-2">
                            Turn audio into edited,
                        </h2>
                        <h2
                            className="text-4xl sm:text-5xl md:text-[60px] font-bold leading-tight sm:leading-[60px] tracking-[-1.5px] bg-clip-text text-transparent"
                            style={{
                                backgroundImage: "linear-gradient(90deg, rgb(166, 132, 255) 0%, rgb(194, 122, 255) 100%)"
                            }}
                        >
                            publish-ready videos
                        </h2>
                    </div>

                    {/* Subheading */}
                    <p className="text-[#a1a1a1] text-base sm:text-lg md:text-xl leading-7 text-center mb-8 max-w-[672px] mx-auto">
                        Upload your audio, add reference images, and let AI automatically edit and stitch your content into platform-optimized videos.
                    </p>

                    {/* CTA Buttons */}
                    <div className="flex gap-4 justify-center mb-12">
                        <Link
                            href="/create"
                            className="bg-[#7f22fe] text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:opacity-90 transition-opacity"
                        >
                            <img alt="Sparkle icon" className="w-4 h-4" src={imgIcon1} loading="lazy" />
                            <span className="text-sm">Create New Video</span>
                        </Link>
                        <Link
                            href="/dashboard"
                            className="bg-[rgba(38,38,38,0.3)] border border-[#262626] text-[#fafafa] px-6 py-2 rounded-lg hover:opacity-90 transition-opacity"
                        >
                            <span className="text-sm">View Dashboard</span>
                        </Link>
                    </div>

                    {/* Process Steps */}
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 sm:gap-4 mb-12">
                        {/* Step 1 */}
                        <div className="flex gap-4">
                            <div className="bg-[#262626] border border-[rgba(38,38,38,0.4)] rounded-[10px] w-12 h-12 flex items-center justify-center flex-shrink-0">
                                <img alt="Upload icon" className="w-5 h-5" src={imgIcon2} loading="lazy" />
                            </div>
                            <div className="flex flex-col gap-1">
                                <span className="text-[#a1a1a1] text-xs font-mono">01</span>
                                <h3 className="text-[#fafafa] text-base">Upload</h3>
                                <p className="text-[#a1a1a1] text-sm leading-5">
                                    Add your audio file and optional reference images
                                </p>
                            </div>
                        </div>

                        {/* Step 2 */}
                        <div className="flex gap-4">
                            <div className="bg-[#262626] border border-[rgba(38,38,38,0.4)] rounded-[10px] w-12 h-12 flex items-center justify-center flex-shrink-0">
                                <img alt="Edit icon" className="w-5 h-5" src={imgIcon3} loading="lazy" />
                            </div>
                            <div className="flex flex-col gap-1">
                                <span className="text-[#a1a1a1] text-xs font-mono">02</span>
                                <h3 className="text-[#fafafa] text-base">Edit</h3>
                                <p className="text-[#a1a1a1] text-sm leading-5">
                                    AI analyzes content and intelligently edits segments
                                </p>
                            </div>
                        </div>

                        {/* Step 3 */}
                        <div className="flex gap-4">
                            <div className="bg-[#262626] border border-[rgba(38,38,38,0.4)] rounded-[10px] w-12 h-12 flex items-center justify-center flex-shrink-0">
                                <img alt="Publish icon" className="w-5 h-5" src={imgIcon4} loading="lazy" />
                            </div>
                            <div className="flex flex-col gap-1">
                                <span className="text-[#a1a1a1] text-xs font-mono">03</span>
                                <h3 className="text-[#fafafa] text-base">Publish</h3>
                                <p className="text-[#a1a1a1] text-sm leading-5">
                                    Export to TikTok, YouTube Shorts, or Instagram Reels
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Audio Waveform Visual */}
                    <div className="bg-gradient-to-r from-[rgba(38,38,38,0.3)] via-[rgba(38,38,38,0.5)] to-[rgba(38,38,38,0.3)] border border-[rgba(38,38,38,0.4)] rounded-[10px] p-3 sm:p-4 overflow-hidden relative">
                        <div className="flex gap-0.5 sm:gap-1 items-center h-[80px] sm:h-[126px]">
                            {[45.301, 37.803, 54.344, 66.816, 83.754, 96.514, 100.798, 97.842, 88.488, 75.784, 66.215, 63.001].map((height, index) => (
                                <div
                                    key={index}
                                    className="flex-1 bg-gradient-to-t from-[rgba(142,81,255,0.3)] to-[rgba(173,70,255,0.3)] rounded-md"
                                    style={{ height: `${(height / 126) * 100}%` }}
                                />
                            ))}
                        </div>
                        <div className="absolute left-[1.61px] top-0 w-1 h-full bg-gradient-to-b from-transparent via-[#a684ff] to-transparent" />
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="border-t border-[rgba(38,38,38,0.4)] h-[69px] flex items-center justify-center">
                <p className="text-[#a1a1a1] text-sm text-center">
                    EVidAi © 2026 — Fast, intelligent, creator-first
                </p>
            </footer>
        </div>
    );
}
