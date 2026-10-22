"use client";
export default function ErrorPage({ reset }: { reset: () => void }) {
  const ar =
    typeof document !== "undefined" && document.documentElement.lang === "ar";
  return (
    <main className="fatal">
      <h1>{ar ? "تعذّر فتح الصفحة" : "We couldn’t open this page"}</h1>
      <p>
        {ar
          ? "يرجى إعادة المحاولة. بياناتك المحفوظة ستبقى متاحة."
          : "Please try again. Your saved entries remain available."}
      </p>
      <button className="button primary" onClick={reset}>
        {ar ? "إعادة المحاولة" : "Try again"}
      </button>
    </main>
  );
}
