export function AppHeader() {
  return (
    <header className="border-b border-black/5 bg-white/55 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4 lg:px-10">
        <div>
          <p className="font-serif text-2xl tracking-tight text-slate-950">
            Simple Mercurio Forms
          </p>
          <p className="text-sm text-slate-600">Next.js client workspace</p>
        </div>
        <div className="rounded-full border border-slate-200 bg-white/80 px-3 py-1 text-sm text-slate-600 shadow-sm">
          apps/web
        </div>
      </div>
    </header>
  );
}