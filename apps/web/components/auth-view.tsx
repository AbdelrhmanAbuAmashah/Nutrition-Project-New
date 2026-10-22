"use client";
import { useState } from "react";
import {
  ArrowRight,
  Check,
  Eye,
  EyeOff,
  ShieldCheck,
  Sprout,
} from "lucide-react";
import { api } from "@/lib/api";
import type { Profile } from "@/lib/types";
import { ErrorNotice, LanguageButton, Logo, Spinner, useUI } from "./ui";

export function AuthView({
  onSuccess,
}: {
  onSuccess: (profile: Profile) => void;
}) {
  const { t, locale } = useUI();
  const [mode, setMode] = useState<"login" | "signup">("signup");
  const [visible, setVisible] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>(null);
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    setError(null);
    setBusy(true);
    try {
      onSuccess(
        await api<Profile>(
          `/auth/${mode === "signup" ? "register" : "login"}`,
          {
            method: "POST",
            body: JSON.stringify({
              email: form.get("email"),
              password: form.get("password"),
              ...(mode === "signup"
                ? {
                    display_name: form.get("name"),
                    locale,
                    accept_privacy: form.get("privacy") === "on",
                  }
                : {}),
            }),
          },
        ),
      );
    } catch (e) {
      setError(e);
    } finally {
      setBusy(false);
    }
  }
  return (
    <main className="auth-layout">
      <section className="auth-story">
        <Logo light />
        <div className="auth-story-copy">
          <span className="eyebrow">
            <Sprout size={15} />
            {t("brandLine")}
          </span>
          <h1>{t("authPanelTitle")}</h1>
          <p>{t("authPanelSub")}</p>
          <div className="bowl-art" aria-hidden="true">
            <div className="plate">
              <span className="grain g1" />
              <span className="grain g2" />
              <span className="grain g3" />
              <span className="veg v1" />
              <span className="veg v2" />
              <span className="veg v3" />
              <span className="tomato t1" />
              <span className="tomato t2" />
              <span className="tomato t3" />
              <span className="herb h1" />
              <span className="herb h2" />
              <span className="herb h3" />
            </div>
            <span className="art-note">
              <LeafIcon />
              {t("sourceBacked")}
            </span>
          </div>
        </div>
        <div className="auth-promises">
          {(["authFeature1", "authFeature2", "authFeature3"] as const).map(
            (key) => (
              <span key={key}>
                <Check size={14} />
                {t(key)}
              </span>
            ),
          )}
        </div>
      </section>
      <section className="auth-form-panel">
        <header>
          <span className="mobile-brand">
            <Logo />
          </span>
          <LanguageButton />
        </header>
        <div className="auth-form-wrap">
          <span className="tag">{t("welcomeNew")}</span>
          <h2>{t(mode === "signup" ? "signupTitle" : "loginTitle")}</h2>
          <p className="muted">{t("authSub")}</p>
          <div className="auth-tabs">
            <button
              className={mode === "signup" ? "active" : ""}
              onClick={() => {
                setMode("signup");
                setError(null);
              }}
            >
              {t("createAccount")}
            </button>
            <button
              className={mode === "login" ? "active" : ""}
              onClick={() => {
                setMode("login");
                setError(null);
              }}
            >
              {t("signIn")}
            </button>
          </div>
          <form onSubmit={submit} className="stack" key={mode}>
            {mode === "signup" && (
              <label>
                {t("displayName")}
                <input
                  name="name"
                  autoComplete="name"
                  required
                  maxLength={80}
                  placeholder={
                    locale === "ar"
                      ? "كيف نُناديك؟"
                      : "What should we call you?"
                  }
                />
              </label>
            )}
            <label>
              {t("email")}
              <input
                name="email"
                type="email"
                autoComplete="email"
                required
                maxLength={254}
                dir="ltr"
                placeholder="you@example.com"
              />
            </label>
            <label>
              {t("password")}
              <span className="password-field">
                <input
                  name="password"
                  type={visible ? "text" : "password"}
                  autoComplete={
                    mode === "signup" ? "new-password" : "current-password"
                  }
                  required
                  minLength={mode === "signup" ? 12 : 1}
                  maxLength={128}
                  dir="ltr"
                  placeholder={
                    mode === "signup" ? t("passwordHint") : "••••••••••••"
                  }
                />
                <button
                  type="button"
                  aria-label={t(visible ? "hidePassword" : "showPassword")}
                  onClick={() => setVisible(!visible)}
                >
                  {visible ? <EyeOff size={19} /> : <Eye size={19} />}
                </button>
              </span>
            </label>
            {mode === "signup" && (
              <label className="check-label privacy-accept">
                <input name="privacy" type="checkbox" required />
                <span>{t("privacyAccept")}</span>
              </label>
            )}
            <ErrorNotice error={error} />
            <button className="button primary large" disabled={busy}>
              {busy ? (
                <Spinner />
              ) : (
                <>
                  {t(mode === "signup" ? "createAccount" : "signIn")}
                  <ArrowRight size={18} className="directional" />
                </>
              )}
            </button>
          </form>
          <p className="auth-switch">
            {t(mode === "signup" ? "alreadyAccount" : "newHere")}{" "}
            <button
              onClick={() => {
                setMode(mode === "signup" ? "login" : "signup");
                setError(null);
              }}
            >
              {t(mode === "signup" ? "signIn" : "createAccount")}
            </button>
          </p>
          <div className="secure-note">
            <ShieldCheck size={17} />
            {t("authFeature3")}
          </div>
        </div>
        <footer>
          © {new Date().getFullYear()} {t("brand")} ·{" "}
          {locale === "ar"
            ? "مصمّم ليومك، بحبّ ووعي."
            : "Made for your everyday."}
        </footer>
      </section>
    </main>
  );
}
function LeafIcon() {
  return <Sprout size={16} />;
}
