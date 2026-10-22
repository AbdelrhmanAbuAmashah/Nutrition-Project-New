"use client";
import { createContext, useContext } from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { ArrowUpRight, Leaf, LoaderCircle, X } from "lucide-react";
import { ApiError } from "@/lib/api";
import { dictionary, number, TextKey } from "@/lib/i18n";
import type { Locale, Values } from "@/lib/types";

export const UIContext = createContext<{
  locale: Locale;
  setLocale: (locale: Locale) => void;
}>({ locale: "en", setLocale: () => {} });
export function useUI() {
  const ui = useContext(UIContext);
  const words = dictionary(ui.locale);
  return {
    ...ui,
    t: (key: TextKey) => words[key],
    n: (value: unknown, digits = 0) => number(value, ui.locale, digits),
    name: (item: { name_en: string; name_ar: string }) =>
      ui.locale === "ar" ? item.name_ar : item.name_en,
  };
}
export function Logo({ light = false }: { light?: boolean }) {
  const { t } = useUI();
  return (
    <div className={`logo ${light ? "light" : ""}`}>
      <span className="logo-mark">
        <Leaf size={23} strokeWidth={1.8} />
      </span>
      <span>
        {t("brand")}
        <span className="logo-dot">.</span>
      </span>
    </div>
  );
}
export function LanguageButton() {
  const { locale, setLocale, t } = useUI();
  return (
    <button
      className="language-button"
      onClick={() => setLocale(locale === "en" ? "ar" : "en")}
      lang={locale === "en" ? "ar" : "en"}
    >
      {t("language")}
      <span aria-hidden="true">↔</span>
    </button>
  );
}
export function Spinner() {
  return <LoaderCircle className="spin" size={20} aria-hidden="true" />;
}
export function ErrorNotice({ error }: { error: unknown }) {
  const { t } = useUI();
  if (!error) return null;
  const message =
    error instanceof ApiError
      ? error.code === "network"
        ? t("network")
        : error.message
      : t("serviceError");
  return (
    <div className="error-notice" role="alert">
      <span>{message}</span>
      {error instanceof ApiError && error.requestId && (
        <small>
          {t("reference")}: <bdi>{error.requestId.slice(0, 8)}</bdi>
        </small>
      )}
    </div>
  );
}
export function Modal({
  open,
  onClose,
  title,
  description,
  children,
  className = "",
  busy = false,
}: {
  open: boolean;
  onClose: () => void;
  title: string;
  description: string;
  children: React.ReactNode;
  className?: string;
  busy?: boolean;
}) {
  const { t, locale } = useUI();
  return (
    <Dialog.Root
      open={open}
      onOpenChange={(value) => {
        if (!value && !busy) onClose();
      }}
    >
      <Dialog.Portal>
        <Dialog.Overlay className="modal-overlay" />
        <Dialog.Content
          className={`modal ${className}`}
          dir={locale === "ar" ? "rtl" : "ltr"}
          onInteractOutside={(e) => e.preventDefault()}
          onEscapeKeyDown={(e) => {
            if (busy) e.preventDefault();
          }}
        >
          <div className="modal-heading">
            <div>
              <Dialog.Title>{title}</Dialog.Title>
              <Dialog.Description>{description}</Dialog.Description>
            </div>
            <Dialog.Close
              className="icon-button"
              aria-label={t("close")}
              disabled={busy}
            >
              <X size={21} />
            </Dialog.Close>
          </div>
          {children}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
export function NutrientStrip({ values }: { values: Values }) {
  const { t, n } = useUI();
  return (
    <div className="nutrient-strip">
      {(["calories", "protein", "carbs", "fat"] as const).map((key) => (
        <div key={key}>
          <span>{t(key)}</span>
          <strong>
            {values[key] === null
              ? "—"
              : n(values[key], key === "calories" ? 0 : 1)}{" "}
            <small>{t(key === "calories" ? "kcal" : "g")}</small>
          </strong>
        </div>
      ))}
    </div>
  );
}
export function SourceLink({
  url,
  children,
}: {
  url: string;
  children: React.ReactNode;
}) {
  return (
    <a className="source-link" href={url} target="_blank" rel="noreferrer">
      {children}
      <ArrowUpRight size={14} />
    </a>
  );
}
