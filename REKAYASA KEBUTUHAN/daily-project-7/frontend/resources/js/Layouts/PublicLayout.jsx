import { Link, usePage } from '@inertiajs/react';

export default function PublicLayout({ title, children, showIntro = true, subtitle = null }) {
    const user = usePage().props.auth.user;

    return (
        <div className="flex min-h-screen flex-col bg-slate-950 text-white">
            <header className="border-b border-white/10 bg-white/5 backdrop-blur">
                <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-4 sm:px-6 lg:px-8">
                    <Link href="/" className="text-lg font-semibold tracking-wide text-white">
                        StudioBook
                    </Link>

                    <nav className="flex flex-wrap items-center gap-3 text-sm">
                        <Link href={route('studios.index')} className="text-white/80 transition hover:text-white">
                            Studios
                        </Link>
                        {user ? (
                            <>
                                <Link href={route('bookings.index')} className="text-white/80 transition hover:text-white">
                                    Bookings
                                </Link>
                                <Link href={route('forum.index')} className="text-white/80 transition hover:text-white">
                                    Forum
                                </Link>
                                <Link href={route('dashboard')} className="rounded-full border border-white/20 px-4 py-2 text-white transition hover:bg-white hover:text-slate-950">
                                    Dashboard
                                </Link>
                            </>
                        ) : (
                            <>
                                <Link href={route('login')} className="text-white/80 transition hover:text-white">
                                    Login
                                </Link>
                                <Link href={route('register')} className="rounded-full border border-white/20 px-4 py-2 text-white transition hover:bg-white hover:text-slate-950">
                                    Register
                                </Link>
                            </>
                        )}
                    </nav>
                </div>
            </header>

            <main className="flex-1">
                <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
                    {showIntro && (
                        <div className="max-w-3xl">
                            <p className="text-sm uppercase tracking-[0.3em] text-cyan-300">{title}</p>
                            {subtitle && <p className="mt-3 text-base leading-7 text-white/75">{subtitle}</p>}
                        </div>
                    )}

                    <div className={showIntro ? 'mt-10' : ''}>
                        {children}
                    </div>
                </section>
            </main>

            <footer className="border-t border-white/10 bg-black/20">
                <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-2 px-4 py-4 text-xs text-white/60 sm:px-6 lg:px-8">
                    <p>StudioBook</p>
                    <p>Booking studio musik lebih cepat</p>
                </div>
            </footer>
        </div>
    );
}