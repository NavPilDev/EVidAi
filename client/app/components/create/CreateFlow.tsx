'use client';

import { useState } from 'react';
import Link from 'next/link';

export function CreateFlow() {
    const [videoDescription, setVideoDescription] = useState('');
    const [audioFile, setAudioFile] = useState<File | null>(null);
    const [referenceImages, setReferenceImages] = useState<File[]>([]);

    const handleAudioUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            // Check file size (100MB limit)
            const maxSize = 100 * 1024 * 1024; // 100MB in bytes
            if (file.size > maxSize) {
                alert('File size exceeds 100MB limit. Please choose a smaller file.');
                return;
            }
            // Check file type
            const validTypes = ['audio/mp3', 'audio/wav', 'audio/m4a', 'audio/mpeg', 'audio/x-m4a'];
            if (!validTypes.includes(file.type) && !file.name.match(/\.(mp3|wav|m4a)$/i)) {
                alert('Invalid file type. Please upload MP3, WAV, or M4A files only.');
                return;
            }
            setAudioFile(file);
        }
    };

    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = Array.from(e.target.files || []);
        setReferenceImages(prev => [...prev, ...files]);
    };

    const handleContinue = () => {
        // TODO: Navigate to next step or submit form
        console.log('Continue to Media Control', {
            videoDescription,
            audioFile,
            referenceImages,
        });
    };

    return (
        <div className="bg-[#0a0a0a] min-h-screen flex flex-col">
            {/* Header */}
            <header className="bg-[rgba(10,10,10,0.8)] border-b border-[rgba(38,38,38,0.4)] h-[65px] flex items-center justify-between px-6">
                <div className="flex items-center gap-4">
                    <Link
                        href="/"
                        className="flex items-center gap-2 px-2 py-2 text-[#fafafa] text-sm hover:opacity-80 transition-opacity"
                    >
                        <img alt="Back arrow" className="w-4 h-4" src={"/icons/backArrowIcon.svg"} />
                        <span>Back</span>
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

                {/* Step Indicator */}
                <div className="hidden sm:flex items-center gap-2">
                    <div className="bg-[#7f22fe] w-8 h-8 rounded-full flex items-center justify-center">
                        <span className="text-white text-sm">1</span>
                    </div>
                    <div className="bg-[#262626] h-px w-12" />
                    <div className="bg-[#262626] w-8 h-8 rounded-full flex items-center justify-center">
                        <span className="text-[#a1a1a1] text-sm">2</span>
                    </div>
                    <div className="bg-[#262626] h-px flex-1" />
                    <div className="bg-[#262626] w-8 h-8 rounded-full flex items-center justify-center">
                        <span className="text-[#a1a1a1] text-sm">3</span>
                    </div>
                </div>
                <div className="sm:hidden text-[#a1a1a1] text-sm">
                    Step 1 of 3
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-1 flex items-start justify-center pt-16 sm:pt-[113px] pb-12 px-4 sm:px-12">
                <div className="max-w-[848px] w-full flex flex-col gap-6 sm:gap-8">
                    {/* Title Section */}
                    <div className="flex flex-col gap-2">
                        <h2 className="text-2xl sm:text-[30px] font-bold text-[#fafafa] leading-tight sm:leading-[36px]">
                            Describe your video
                        </h2>
                        <p className="text-[#a1a1a1] text-sm sm:text-base leading-6">
                            Tell us what you want to create and upload your source audio
                        </p>
                    </div>

                    {/* Video Description */}
                    <div className="flex flex-col gap-3">
                        <label className="text-[#fafafa] text-sm">Video Description</label>
                        <textarea
                            value={videoDescription}
                            onChange={(e) => setVideoDescription(e.target.value)}
                            placeholder="E.g., Create an engaging educational video about climate change with dynamic visuals and smooth transitions..."
                            className="bg-[rgba(38,38,38,0.3)] border border-[rgba(38,38,38,0.4)] rounded-lg px-3 py-2 h-[120px] text-[#fafafa] text-sm placeholder:text-[#a1a1a1] focus:outline-none focus:ring-2 focus:ring-[#7f22fe] focus:border-transparent resize-none"
                        />
                    </div>

                    {/* Audio File Upload */}
                    <div className="flex flex-col gap-3">
                        <label className="text-[#fafafa] text-sm">
                            Audio File <span className="text-[#a1a1a1]">*</span>
                        </label>
                        <label className="border-2 border-dashed border-[rgba(38,38,38,0.4)] rounded-[10px] h-[168px] flex flex-col items-center justify-center cursor-pointer hover:border-[rgba(142,81,255,0.4)] transition-colors">
                            <input
                                type="file"
                                accept="audio/mp3,audio/wav,audio/m4a,audio/*"
                                onChange={handleAudioUpload}
                                className="hidden"
                            />
                            <div className="bg-[#262626] border border-[rgba(38,38,38,0.4)] rounded-[10px] w-12 h-12 flex items-center justify-center mb-4">
                                <img alt="Upload icon" className="w-5 h-5" src={"/icons/uploadIcon.svg"} loading="lazy" />
                            </div>
                            {audioFile ? (
                                <div className="text-center">
                                    <p className="text-[#fafafa] text-sm mb-1">{audioFile.name}</p>
                                    <p className="text-[#a1a1a1] text-xs">
                                        {(audioFile.size / 1024 / 1024).toFixed(2)} MB
                                    </p>
                                </div>
                            ) : (
                                <>
                                    <p className="text-[#fafafa] text-sm mb-2">Click to upload audio</p>
                                    <p className="text-[#a1a1a1] text-xs">MP3, WAV, M4A up to 100MB</p>
                                </>
                            )}
                        </label>
                    </div>

                    {/* Reference Images Upload */}
                    <div className="flex flex-col gap-3">
                        <label className="text-[#fafafa] text-sm">Reference Images (Optional)</label>
                        <p className="text-[#a1a1a1] text-xs">
                            Upload images to guide the visual style and content of your video
                        </p>
                        <label className="border-2 border-dashed border-[rgba(38,38,38,0.4)] rounded-[10px] h-[120px] flex flex-col items-center justify-center cursor-pointer hover:border-[rgba(142,81,255,0.4)] transition-colors">
                            <input
                                type="file"
                                accept="image/*"
                                multiple
                                onChange={handleImageUpload}
                                className="hidden"
                            />
                            <div className="bg-[#262626] border border-[rgba(38,38,38,0.4)] rounded-[10px] w-10 h-10 flex items-center justify-center mb-3">
                                <img alt="Image icon" className="w-4 h-4" src={"/icons/imageIcon.svg"} loading="lazy" />
                            </div>
                            {referenceImages.length > 0 ? (
                                <p className="text-[#fafafa] text-sm">
                                    {referenceImages.length} image{referenceImages.length > 1 ? 's' : ''} selected
                                </p>
                            ) : (
                                <p className="text-[#a1a1a1] text-sm">Click to add images</p>
                            )}
                        </label>
                        {referenceImages.length > 0 && (
                            <div className="flex flex-wrap gap-2 mt-2">
                                {referenceImages.map((img, index) => (
                                    <div key={index} className="relative">
                                        <img
                                            src={URL.createObjectURL(img)}
                                            alt={`Reference ${index + 1}`}
                                            className="w-20 h-20 object-cover rounded-lg"
                                        />
                                        <button
                                            onClick={() => setReferenceImages(prev => prev.filter((_, i) => i !== index))}
                                            className="absolute -top-2 -right-2 bg-[#262626] text-[#fafafa] rounded-full w-5 h-5 flex items-center justify-center text-xs hover:bg-[#7f22fe] transition-colors"
                                        >
                                            ×
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Continue Button */}
                    <div className="flex justify-end pt-4">
                        <button
                            onClick={handleContinue}
                            disabled={!audioFile}
                            className={`bg-[#7f22fe] text-[#171717] px-6 py-2 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity ${!audioFile ? 'opacity-50 cursor-not-allowed' : ''
                                }`}
                        >
                            Continue to Media Control
                        </button>
                    </div>
                </div>
            </main>
        </div>
    );
}
