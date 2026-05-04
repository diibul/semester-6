import '../css/app.css';

import { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';

const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

function App() {
    const [studios, setStudios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const controller = new AbortController();

        async function loadStudios() {
            try {
                setLoading(true);
                setError('');

                const response = await fetch(`${backendUrl}/api/studios`, {
                    signal: controller.signal,
                });

                if (!response.ok) {
                    throw new Error(`Request gagal dengan status ${response.status}`);
                }

                const payload = await response.json();
                setStudios(Array.isArray(payload.data) ? payload.data : []);
            } catch (error) {
                if (error.name !== 'AbortError') {
                    setError('Gagal memuat data studio dari backend.');
                }
            } finally {
                setLoading(false);
            }
        }

        loadStudios();

        return () => controller.abort();
    }, []);

    const totalAvailableSchedules = useMemo(
        () => studios.reduce((total, studio) => total + (studio.available_schedules_count || 0), 0),
        [studios],
    );

    return (
        <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(34,211,238,0.18),_transparent_34%),linear-gradient(180deg,#08111f_0%,#101827_45%,#0b1220_100%)] text-white">
            <main className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-5 py-6 sm:px-6 lg:px-8">
                <header className="flex flex-col gap-4 rounded-[2rem] border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/20 backdrop-blur sm:p-8 lg:flex-row lg:items-end lg:justify-between">
                    <div>
                        <p className="text-xs uppercase tracking-[0.35em] text-cyan-300">StudioBook</p>
                        <h1 className="mt-3 max-w-2xl text-3xl font-semibold leading-tight sm:text-5xl">
                            Booking studio musik dibuat lebih sederhana untuk project yang kamu bangun.
                        </h1>
                        <p className="mt-4 max-w-2xl text-sm leading-7 text-white/70 sm:text-base">
                            Frontend ini siap dipindah ke Vercel. Data studio diambil dari backend Laravel lewat endpoint JSON.
                        </p>
                    </div>

                    <div className="grid gap-3 sm:grid-cols-3 lg:w-[28rem]">
                        <Stat label="Studio" value={studios.length} />
                        <Stat label="Jadwal aktif" value={totalAvailableSchedules} />
                        <Stat label="Mode" value="Vercel" />
                    </div>
                </header>

                <section className="mt-6 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
                    <div className="rounded-[2rem] border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/20">
                        <div className="flex items-center justify-between gap-3">
                            <div>
                                <p className="text-xs uppercase tracking-[0.3em] text-cyan-300">Public studios</p>
                                <h2 className="mt-2 text-2xl font-semibold">Daftar studio dari backend</h2>
                            </div>

                            <a
                                href={backendUrl}
                                target="_blank"
                                rel="noreferrer"
                                className="rounded-full border border-cyan-300/30 bg-cyan-300/10 px-4 py-2 text-sm font-medium text-cyan-100 transition hover:bg-cyan-300/20"
                            >
                                Buka backend
                            </a>
                        </div>

                        <div className="mt-6">
                            {loading && (
                                <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                                    <LoadingCard />
                                    <LoadingCard />
                                    <LoadingCard />
                                </div>
                            )}

                            {error && !loading && (
                                <div className="rounded-2xl border border-rose-400/30 bg-rose-500/10 p-5 text-sm text-rose-100">
                                    {error}
                                </div>
                            )}

                            {!loading && !error && studios.length === 0 && (
                                <div className="rounded-2xl border border-white/10 bg-black/20 p-6 text-sm text-white/70">
                                    Belum ada studio di database backend.
                                </div>
                            )}

                            {!loading && !error && studios.length > 0 && (
                                <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                                    {studios.map((studio) => (
                                        <article
                                            key={studio.id}
                                            className="group rounded-[1.75rem] border border-white/10 bg-[#0b1324]/90 p-5 transition duration-300 hover:-translate-y-1 hover:border-cyan-300/30 hover:shadow-[0_0_0_1px_rgba(34,211,238,0.15)]"
                                        >
                                            <div className="flex items-start justify-between gap-3">
                                                <div>
                                                    <p className="text-[0.7rem] uppercase tracking-[0.3em] text-cyan-300/90">
                                                        {studio.type}
                                                    </p>
                                                    <h3 className="mt-2 text-xl font-semibold text-white">{studio.name}</h3>
                                                </div>

                                                <span className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-xs font-medium text-cyan-100">
                                                    {studio.available_schedules_count} slot
                                                </span>
                                            </div>

                                            <p className="mt-4 line-clamp-3 text-sm leading-6 text-white/70">
                                                {studio.description}
                                            </p>

                                            <div className="mt-4 flex items-center justify-between gap-3 text-sm text-white/65">
                                                <span>{studio.location}</span>
                                                <span>Rp {Number(studio.price_per_hour).toLocaleString('id-ID')} / jam</span>
                                            </div>

                                            <a
                                                href={`${backendUrl}/studios/${studio.slug}`}
                                                target="_blank"
                                                rel="noreferrer"
                                                className="mt-5 inline-flex rounded-full bg-cyan-300 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-200"
                                            >
                                                Lihat di backend
                                            </a>
                                        </article>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>

                    <aside className="grid gap-6">
                        <div className="overflow-hidden rounded-[2rem] border border-white/10 bg-white/5 shadow-2xl shadow-black/20">
                            <img
                                src="https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=1200&q=80"
                                alt="Studio musik"
                                className="h-72 w-full object-cover"
                                loading="lazy"
                            />
                        </div>

                        <div className="rounded-[2rem] border border-cyan-300/15 bg-cyan-400/10 p-6 ring-1 ring-cyan-300/10">
                            <p className="text-xs uppercase tracking-[0.3em] text-cyan-200">Langkah deploy</p>
                            <ol className="mt-4 list-decimal space-y-3 pl-5 text-sm leading-6 text-white/80 marker:text-cyan-200">
                                <li>Backend Laravel tetap di host PHP.</li>
                                <li>Frontend ini dipush ke Vercel.</li>
                                <li>Set <span className="font-semibold text-cyan-200">VITE_BACKEND_URL</span> ke URL backend.</li>
                            </ol>
                        </div>
                    </aside>
                </section>
            </main>
        </div>
    );
}

function Stat({ label, value }) {
    return (
        <div className="rounded-2xl border border-white/10 bg-black/20 px-4 py-3">
            <p className="text-[0.7rem] uppercase tracking-[0.28em] text-white/45">{label}</p>
            <p className="mt-2 text-2xl font-semibold text-white">{value}</p>
        </div>
    );
}

function LoadingCard() {
    return <div className="h-56 animate-pulse rounded-[1.75rem] border border-white/10 bg-white/5" />;
}

createRoot(document.getElementById('app')).render(<App />);