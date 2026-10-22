"use client";
import { useState } from "react";
import {
  Check,
  Download,
  Globe2,
  Heart,
  Plus,
  ShieldCheck,
  SlidersHorizontal,
  Trash2,
  UserRound,
  X,
} from "lucide-react";
import { api, ApiError, normalizeNumber } from "@/lib/api";
import type { Options, Profile, Restriction } from "@/lib/types";
import { ErrorNotice, Modal, Spinner, useUI } from "./ui";

export function ProfileView({
  profile,
  options,
  onSave,
  onDelete,
}: {
  profile: Profile;
  options: Options;
  onSave: (p: Profile) => void;
  onDelete: () => void;
}) {
  const { t, locale, name } = useUI();
  const [p, setP] = useState(profile);
  const [displayName, setDisplayName] = useState(profile.user.display_name);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const [deleting, setDeleting] = useState(false);
  const [password, setPassword] = useState("");
  const [substance, setSubstance] = useState("");
  const [kind, setKind] = useState<Restriction["kind"]>("allergy");
  const change = (key: keyof Profile, value: unknown) =>
    setP((old) => ({ ...old, [key]: value }));
  async function save(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const fields = {
        display_name: displayName,
        locale,
        country: p.country,
        timezone: p.timezone,
        units: p.units,
        goal: p.goal,
        target_origin: p.target_origin,
        calorie_target: p.calorie_target
          ? normalizeNumber(p.calorie_target)
          : null,
        protein_target: p.protein_target
          ? normalizeNumber(p.protein_target)
          : null,
        carbs_target: p.carbs_target ? normalizeNumber(p.carbs_target) : null,
        fat_target: p.fat_target ? normalizeNumber(p.fat_target) : null,
        allergy_status: p.allergy_status,
        restrictions: p.restrictions.map(({ substance_id, kind }) => ({
          substance_id,
          kind,
        })),
        conditions: p.conditions,
        preferences: p.preferences,
        revision: p.revision,
        complete_onboarding: true,
      };
      const saved = await api<Profile>("/profile", {
        method: "PATCH",
        body: JSON.stringify(fields),
      });
      setP(saved);
      onSave(saved);
    } catch (e) {
      setError(e);
    } finally {
      setBusy(false);
    }
  }
  async function exportData() {
    setError(null);
    try {
      const data = await api("/account/export");
      const url = URL.createObjectURL(
        new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }),
      );
      const a = document.createElement("a");
      a.href = url;
      a.download = "nour-export.json";
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(e);
    }
  }
  async function deleteAccount() {
    setError(null);
    setBusy(true);
    try {
      await api("/account", {
        method: "DELETE",
        body: JSON.stringify({ password }),
      });
      onDelete();
    } catch (e) {
      setError(e);
    } finally {
      setBusy(false);
    }
  }
  function addRestriction() {
    if (!substance) return;
    if (
      p.restrictions.some(
        (r) => r.substance_id === substance && r.kind === kind,
      )
    )
      return;
    change("restrictions", [
      ...p.restrictions,
      { substance_id: substance, kind },
    ]);
    if (kind === "allergy") change("allergy_status", "recorded");
    setSubstance("");
  }
  return (
    <>
      <div className="page-heading">
        <div>
          <span className="eyebrow">{t("profile")}</span>
          <h1>{t("profileTitle")}</h1>
          <p>{t("profileSub")}</p>
        </div>
        <div className="heading-icon">
          <UserRound size={29} />
        </div>
      </div>
      <form onSubmit={save} className="profile-layout">
        <div className="profile-main">
          <section className="panel profile-section">
            <div className="section-title">
              <span className="section-icon">
                <Globe2 size={19} />
              </span>
              <h2>{t("basics")}</h2>
            </div>
            <div className="form-grid">
              <label>
                {t("displayName")}
                <input
                  required
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  maxLength={80}
                  autoComplete="name"
                />
              </label>
              <label>
                {t("country")}
                <select
                  value={p.country}
                  onChange={(e) => {
                    change("country", e.target.value);
                    change(
                      "timezone",
                      e.target.value === "SA" ? "Asia/Riyadh" : "Asia/Amman",
                    );
                  }}
                >
                  <option value="JO">{t("jordan")}</option>
                  <option value="SA">{t("saudi")}</option>
                </select>
              </label>
              <label>
                {t("timezone")}
                <select
                  value={p.timezone}
                  onChange={(e) => change("timezone", e.target.value)}
                >
                  <option value="Asia/Amman">Asia/Amman</option>
                  <option value="Asia/Riyadh">Asia/Riyadh</option>
                  {!["Asia/Amman", "Asia/Riyadh"].includes(p.timezone) && (
                    <option value={p.timezone}>{p.timezone}</option>
                  )}
                </select>
              </label>
              <label>
                {t("goal")}
                <select
                  value={p.goal}
                  onChange={(e) => change("goal", e.target.value)}
                >
                  {(["understand", "maintain", "lose", "gain"] as const).map(
                    (g) => (
                      <option key={g} value={g}>
                        {t(g)}
                      </option>
                    ),
                  )}
                </select>
              </label>
            </div>
            <h3 className="field-section-label">{t("preferences")}</h3>
            <div className="preference-pills">
              {(["vegetarian", "vegan", "halal", "pescatarian"] as const).map(
                (pref) => (
                  <button
                    type="button"
                    key={pref}
                    className={p.preferences.includes(pref) ? "selected" : ""}
                    aria-pressed={p.preferences.includes(pref)}
                    onClick={() =>
                      change(
                        "preferences",
                        p.preferences.includes(pref)
                          ? p.preferences.filter((v) => v !== pref)
                          : [...p.preferences, pref],
                      )
                    }
                  >
                    {p.preferences.includes(pref) && <Check size={14} />}{" "}
                    {t(pref)}
                  </button>
                ),
              )}
            </div>
          </section>
          <section className="panel profile-section">
            <div className="section-title">
              <span className="section-icon peach">
                <SlidersHorizontal size={19} />
              </span>
              <h2>{t("goals")}</h2>
            </div>
            <p className="section-description">{t("goalsSub")}</p>
            <div className="form-grid">
              {(["calories", "protein", "carbs", "fat"] as const).map((key) => {
                const field =
                  key === "calories"
                    ? "calorie_target"
                    : (`${key}_target` as
                        "protein_target" | "carbs_target" | "fat_target");
                return (
                  <label key={key}>
                    {t(key)} ({t(key === "calories" ? "kcal" : "g")})
                    <input
                      inputMode="decimal"
                      value={p[field] || ""}
                      onChange={(e) => change(field, e.target.value)}
                      placeholder={t("optional")}
                    />
                  </label>
                );
              })}
              <label>
                {t("targetOrigin")}
                <select
                  value={p.target_origin}
                  onChange={(e) => change("target_origin", e.target.value)}
                >
                  <option value="user">{t("byUser")}</option>
                  <option value="professional">{t("byProfessional")}</option>
                </select>
              </label>
            </div>
          </section>
          <section className="panel profile-section">
            <div className="section-title">
              <span className="section-icon lilac">
                <ShieldCheck size={19} />
              </span>
              <h2>{t("restrictions")}</h2>
            </div>
            <p className="section-description">{t("restrictionSub")}</p>
            <label>
              {t("allergyStatus")}
              <select
                value={p.allergy_status}
                onChange={(e) => change("allergy_status", e.target.value)}
              >
                <option value="unknown">{t("allergyUnknown")}</option>
                <option value="none">{t("allergyNone")}</option>
                <option value="recorded">{t("allergyRecorded")}</option>
              </select>
            </label>
            <div className="restriction-list">
              {p.restrictions.map((r, i) => (
                <div
                  key={`${r.kind}-${r.substance_id}`}
                  className="restriction-row"
                >
                  <div>
                    <strong>
                      {name(
                        options.substances.find(
                          (s) => s.id === r.substance_id,
                        ) || {
                          name_en: r.substance_id,
                          name_ar: r.substance_id,
                        },
                      )}
                    </strong>
                    <span
                      className={`tag ${r.kind === "allergy" ? "peach" : ""}`}
                    >
                      {t(r.kind)}
                    </span>
                  </div>
                  <button
                    type="button"
                    className="icon-button"
                    aria-label={`${t("remove")} ${r.substance_id}`}
                    onClick={() =>
                      change(
                        "restrictions",
                        p.restrictions.filter((_, j) => i !== j),
                      )
                    }
                  >
                    <X size={17} />
                  </button>
                </div>
              ))}
            </div>
            <div className="restriction-add">
              <label>
                <span className="sr-only">{t("chooseSubstance")}</span>
                <select
                  value={substance}
                  onChange={(e) => setSubstance(e.target.value)}
                >
                  <option value="">{t("chooseSubstance")}</option>
                  {options.substances.map((s) => (
                    <option value={s.id} key={s.id}>
                      {name(s)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                <span className="sr-only">{t("restrictions")}</span>
                <select
                  value={kind}
                  onChange={(e) =>
                    setKind(e.target.value as Restriction["kind"])
                  }
                >
                  {(["allergy", "intolerance", "dislike"] as const).map((v) => (
                    <option key={v} value={v}>
                      {t(v)}
                    </option>
                  ))}
                </select>
              </label>
              <button
                type="button"
                className="button secondary"
                onClick={addRestriction}
                disabled={!substance}
              >
                <Plus size={17} />
                {t("addRestriction")}
              </button>
            </div>
          </section>
          <section className="panel profile-section">
            <div className="section-title">
              <span className="section-icon">
                <Heart size={19} />
              </span>
              <h2>{t("conditions")}</h2>
            </div>
            <p className="section-description">{t("conditionSub")}</p>
            <div className="stack">
              {options.conditions.map((c) => (
                <label className="check-label" key={c.id}>
                  <input
                    type="checkbox"
                    checked={p.conditions.includes(c.id)}
                    onChange={(e) =>
                      change(
                        "conditions",
                        e.target.checked
                          ? [...p.conditions, c.id]
                          : p.conditions.filter((v) => v !== c.id),
                      )
                    }
                  />
                  <span>{name(c)}</span>
                </label>
              ))}
            </div>
          </section>
          <ErrorNotice error={!deleting ? error : null} />
          <div className="profile-save">
            <p>{t("confirmProfileFacts")}</p>
            <button className="button primary" disabled={busy}>
              {busy ? <Spinner /> : <Check size={17} />}{" "}
              {t(profile.onboarding_completed ? "save" : "getStarted")}
            </button>
          </div>
        </div>
        <aside className="profile-aside">
          <div className="panel privacy-card">
            <ShieldCheck size={27} />
            <h2>{t("privacy")}</h2>
            <p>{t("authFeature3")}</p>
            <button
              type="button"
              className="button secondary"
              onClick={exportData}
            >
              <Download size={17} />
              {t("exportData")}
            </button>
            <button
              type="button"
              className="text-button danger"
              onClick={() => {
                setError(null);
                setDeleting(true);
              }}
            >
              <Trash2 size={16} />
              {t("deleteAccount")}
            </button>
          </div>
          <div className="aside-note">
            <Heart size={20} />
            <p>{t("pendingClinical")}</p>
          </div>
        </aside>
      </form>
      <Modal
        open={deleting}
        onClose={() => {
          setDeleting(false);
          setPassword("");
          setError(null);
        }}
        title={t("deleteAccount")}
        description={t("deleteAccountText")}
        className="small-modal"
        busy={busy}
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            void deleteAccount();
          }}
          className="stack modal-body"
        >
          <label>
            {t("password")}
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              dir="ltr"
            />
          </label>
          <ErrorNotice error={error} />
          <button className="button danger-button" disabled={busy}>
            {busy ? <Spinner /> : <Trash2 size={17} />} {t("deleteAccount")}
          </button>
        </form>
      </Modal>
    </>
  );
}
