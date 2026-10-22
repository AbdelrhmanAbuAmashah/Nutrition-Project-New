"use client";
import { useEffect, useState } from "react";
import {
  AlertCircle,
  Check,
  CheckCheck,
  ChevronRight,
  ExternalLink,
  Flame,
  Leaf,
  Plus,
  Search,
  ShieldQuestion,
  Trash2,
  UtensilsCrossed,
  X,
} from "lucide-react";
import {
  api,
  normalizeNumber,
  zonedDateTime,
  localDay,
  randomKey,
} from "@/lib/api";
import type {
  Food,
  Meal,
  Preview,
  Profile,
  Recipe,
  Selection,
} from "@/lib/types";
import {
  ErrorNotice,
  Modal,
  NutrientStrip,
  SourceLink,
  Spinner,
  useUI,
} from "./ui";

export function MealDrawer({
  open,
  onClose,
  onSaved,
  profile,
  day,
  initialRecipe,
}: {
  open: boolean;
  onClose: () => void;
  onSaved: () => void;
  profile: Profile;
  day: string;
  initialRecipe?: Recipe;
}) {
  const { t, name, n } = useUI();
  const [q, setQ] = useState("");
  const [category, setCategory] = useState("");
  const [foods, setFoods] = useState<Food[]>([]);
  const [searching, setSearching] = useState(false);
  const [items, setItems] = useState<Selection[]>(
    initialRecipe
      ? [
          {
            key: randomKey(),
            type: "recipe",
            item: initialRecipe,
            grams: initialRecipe.serving_grams,
            evidence: "user_entered",
          },
        ]
      : [],
  );
  const [type, setType] = useState("lunch");
  const [title, setTitle] = useState("");
  const [preview, setPreview] = useState<Preview | null>(null);
  const [previewing, setPreviewing] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const [searchError, setSearchError] = useState<unknown>(null);
  const [busy, setBusy] = useState(false);
  const [idempotency, setIdempotency] = useState(randomKey);
  const [detail, setDetail] = useState<Food | null>(null);
  const [clock, setClock] = useState(() =>
    day === localDay(profile.timezone)
      ? new Intl.DateTimeFormat("en-GB", {
          timeZone: profile.timezone,
          hour: "2-digit",
          minute: "2-digit",
          hourCycle: "h23",
        }).format(new Date())
      : "12:00",
  );
  const consumedAt = clock ? zonedDateTime(day, clock, profile.timezone) : "";
  const normalized = items.map((item) => ({
    ...item,
    normalized: normalizeNumber(item.grams),
  }));
  const valid =
    !!clock &&
    normalized.length > 0 &&
    normalized.every(
      (i) =>
        /^\d+(\.\d{1,3})?$/.test(i.normalized) &&
        Number(i.normalized) > 0 &&
        Number(i.normalized) <= 10000,
    );
  const payload = {
    title: title.trim() || t(type as "lunch"),
    meal_type: type,
    consumed_at: consumedAt,
    items: normalized.map((item) => ({
      [item.type === "food" ? "food_version_id" : "recipe_version_id"]:
        item.item.id,
      grams: item.normalized,
      evidence: item.evidence,
    })),
  };
  const payloadString = JSON.stringify(payload);
  useEffect(() => {
    const controller = new AbortController();
    const timer = setTimeout(() => {
      setSearching(true);
      setSearchError(null);
      api<{ items: Food[] }>(
        `/foods?q=${encodeURIComponent(q)}${category ? `&category=${category}` : ""}`,
        { signal: controller.signal },
      )
        .then((result) => setFoods(result.items))
        .catch((e) => {
          if (e.name !== "AbortError") setSearchError(e);
        })
        .finally(() => {
          if (!controller.signal.aborted) setSearching(false);
        });
    }, 180);
    return () => {
      clearTimeout(timer);
      controller.abort();
    };
  }, [q, category]);
  useEffect(() => {
    setPreview(null);
    setError(null);
    setIdempotency(randomKey());
    if (!valid) {
      setPreviewing(false);
      return;
    }
    const controller = new AbortController();
    setPreviewing(true);
    const timer = setTimeout(() => {
      api<Preview>("/meals/preview", {
        method: "POST",
        body: payloadString,
        signal: controller.signal,
      })
        .then(setPreview)
        .catch((e) => {
          if (e.name !== "AbortError") setError(e);
        })
        .finally(() => {
          if (!controller.signal.aborted) setPreviewing(false);
        });
    }, 220);
    return () => {
      clearTimeout(timer);
      controller.abort();
    };
  }, [payloadString, valid]);
  function add(food: Food) {
    setItems((old) => {
      const found = old.find((i) => i.type === "food" && i.item.id === food.id);
      return found
        ? old.map((i) =>
            i === found
              ? {
                  ...i,
                  grams: String(Number(normalizeNumber(i.grams) || 0) + 100),
                }
              : i,
          )
        : [
            ...old,
            {
              key: randomKey(),
              type: "food",
              item: food,
              grams: "100",
              evidence: "user_entered",
            },
          ];
    });
  }
  function change(key: string, patch: Partial<Selection>) {
    setItems((old) => old.map((i) => (i.key === key ? { ...i, ...patch } : i)));
  }
  async function save() {
    if (!valid || !preview) return;
    setBusy(true);
    setError(null);
    try {
      const meal = await api<Meal>("/meals", {
        method: "POST",
        body: payloadString,
        headers: { "Idempotency-Key": idempotency },
      });
      await api(`/meals/${meal.id}/confirm`, { method: "POST" });
      onSaved();
    } catch (e) {
      setError(e);
    } finally {
      setBusy(false);
    }
  }
  return (
    <Modal
      open={open}
      onClose={onClose}
      title={t("mealBuilder")}
      description={t("mealBuilderSub")}
      className="meal-modal"
      busy={busy}
    >
      <div className="meal-workspace">
        <section className="catalog-pane">
          <div className="search-field">
            <Search size={19} />
            <input
              aria-label={t("searchFood")}
              placeholder={t("searchFood")}
              value={q}
              onChange={(e) => setQ(e.target.value)}
            />
            {q && (
              <button
                className="icon-button"
                aria-label={t("remove")}
                onClick={() => setQ("")}
              >
                <X size={16} />
              </button>
            )}
          </div>
          <div className="catalog-categories">
            {(
              [
                "",
                "fruit",
                "vegetables",
                "protein",
                "grains",
                "pantry",
              ] as const
            ).map((cat) => (
              <button
                key={cat}
                className={category === cat ? "active" : ""}
                onClick={() => setCategory(cat)}
                aria-pressed={category === cat}
              >
                {t(
                  cat === ""
                    ? "all"
                    : cat === "protein"
                      ? "proteinCategory"
                      : cat,
                )}
              </button>
            ))}
          </div>
          <ErrorNotice error={searchError} />
          <div className="food-results" aria-busy={searching}>
            {searching && (
              <div className="search-loading">
                <Spinner />
              </div>
            )}
            {!searching && foods.length === 0 && (
              <p className="empty-search">{t("unknown")}</p>
            )}
            {foods.map((food) => (
              <div className="food-result" key={food.id}>
                <span className={`food-symbol ${food.category}`}>
                  <FoodIcon category={food.category} />
                </span>
                <div className="food-result-text">
                  <button className="food-name" onClick={() => setDetail(food)}>
                    {name(food)}
                  </button>
                  <span>
                    {food.nutrients.calories === null
                      ? "—"
                      : n(food.nutrients.calories)}{" "}
                    {t("kcal")} <span className="dot">·</span> {t("per100")}
                  </span>
                </div>
                <button
                  className="add-food"
                  aria-label={`${t("add")} ${name(food)}`}
                  onClick={() => add(food)}
                  disabled={busy}
                >
                  <Plus size={19} />
                </button>
              </div>
            ))}
          </div>
          <p className="catalog-footer">
            <CheckCheck size={15} />
            USDA FoodData Central · {t("sourceBacked")}
          </p>
        </section>
        <section className="plate-pane">
          <div className="plate-title">
            <h3>{t("selected")}</h3>
            <span className="count-pill">{n(items.length)}</span>
          </div>
          {items.length === 0 ? (
            <div className="empty-plate">
              <span>
                <UtensilsCrossed size={29} />
              </span>
              <h3>{t("nothingSelected")}</h3>
              <p>{t("nothingSelectedSub")}</p>
            </div>
          ) : (
            <>
              <div className="form-grid meal-meta">
                <label>
                  {t("mealName")}
                  <input
                    placeholder={t(type as "lunch")}
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    maxLength={120}
                    disabled={busy}
                  />
                </label>
                <label>
                  {t("mealType")}
                  <select
                    value={type}
                    onChange={(e) => setType(e.target.value)}
                    disabled={busy}
                  >
                    {(["breakfast", "lunch", "dinner", "snack"] as const).map(
                      (v) => (
                        <option key={v} value={v}>
                          {t(v)}
                        </option>
                      ),
                    )}
                  </select>
                </label>
              </div>
              <label className="meal-time">
                {t("mealTime")} · {profile.timezone}
                <input
                  type="time"
                  required
                  value={clock}
                  onChange={(e) => setClock(e.target.value)}
                  disabled={busy}
                />
              </label>
              <div className="selected-items">
                {items.map((item) => (
                  <div className="selected-item" key={item.key}>
                    <div className="selected-item-name">
                      <strong>{name(item.item)}</strong>
                      <button
                        className="icon-button"
                        aria-label={`${t("remove")} ${name(item.item)}`}
                        onClick={() =>
                          setItems((old) =>
                            old.filter((i) => i.key !== item.key),
                          )
                        }
                        disabled={busy}
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                    <div className="quantity-row">
                      <label>
                        {t("quantity")}
                        <span className="quantity-input">
                          <input
                            inputMode="decimal"
                            aria-label={`${t("quantity")} ${name(item.item)}`}
                            value={item.grams}
                            onChange={(e) =>
                              change(item.key, { grams: e.target.value })
                            }
                            disabled={busy}
                          />
                          <span>{t("g")}</span>
                        </span>
                      </label>
                      <label>
                        {t("evidence")}
                        <select
                          value={item.evidence}
                          onChange={(e) =>
                            change(item.key, {
                              evidence: e.target.value as Selection["evidence"],
                            })
                          }
                          disabled={busy}
                        >
                          <option value="user_entered">{t("entered")}</option>
                          <option value="weighed">{t("measured")}</option>
                        </select>
                      </label>
                    </div>
                  </div>
                ))}
              </div>
              {!valid && (
                <p className="inline-validation" role="alert">
                  {t("gramsInvalid")}
                </p>
              )}
              <div className="preview-area" aria-live="polite">
                {previewing ? (
                  <p className="calculating">
                    <Spinner />
                    {t("calculating")}
                  </p>
                ) : (
                  preview && (
                    <>
                      <NutrientStrip values={preview.nutrition.values} />
                      {!preview.nutrition.complete && (
                        <div className="note amber">{t("incomplete")}</div>
                      )}
                      <RestrictionNote status={preview.restrictions.status} />
                    </>
                  )
                )}
              </div>
            </>
          )}
          <ErrorNotice error={error} />
          <div className="plate-save">
            <p>{t("draftInfo")}</p>
            <button
              className="button primary large"
              onClick={save}
              disabled={!valid || !preview || previewing || busy}
            >
              {busy ? <Spinner /> : <Check size={18} />} {t("confirmMeal")}
            </button>
          </div>
        </section>
      </div>
      <Modal
        open={!!detail}
        onClose={() => setDetail(null)}
        title={detail ? name(detail) : ""}
        description={t("sourceDetails")}
        className="small-modal"
      >
        <div className="modal-body stack">
          {detail && (
            <>
              <NutrientStrip values={detail.nutrients} />
              <dl className="source-facts">
                <dt>{t("preparedState")}</dt>
                <dd>{detail.preparation}</dd>
                <dt>{t("sourceVersion")}</dt>
                <dd>
                  FDC {detail.source.external_id} · {detail.source.data_type} ·{" "}
                  {detail.source.source_date}
                </dd>
              </dl>
              <SourceLink url={detail.source.url}>
                USDA FoodData Central
              </SourceLink>
            </>
          )}
        </div>
      </Modal>
    </Modal>
  );
}
export function RestrictionNote({ status }: { status: string }) {
  const { t } = useUI();
  const conflict = status === "conflict",
    unknown = status === "unknown";
  return (
    <div className={`restriction-note ${conflict ? "warning" : ""}`}>
      {conflict ? <AlertCircle size={18} /> : <ShieldQuestion size={18} />}
      <div>
        <strong>
          {t(
            conflict
              ? "conflictTitle"
              : unknown
                ? "unknownTitle"
                : "noConflictTitle",
          )}
        </strong>
        <p>
          {t(
            conflict
              ? "conflictText"
              : unknown
                ? "unknownText"
                : "noConflictText",
          )}
        </p>
      </div>
    </div>
  );
}
export function FoodIcon({ category }: { category: string }) {
  return category === "protein" ? (
    <UtensilsCrossed size={21} />
  ) : category === "pantry" ? (
    <Flame size={21} />
  ) : (
    <Leaf size={21} />
  );
}
