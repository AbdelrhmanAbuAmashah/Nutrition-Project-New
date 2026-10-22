"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  ArrowUpRight,
  BookOpen,
  CalendarDays,
  Check,
  ChevronLeft,
  ChevronRight,
  Clock3,
  Flame,
  LayoutDashboard,
  Leaf,
  LogOut,
  Menu,
  Plus,
  ShieldCheck,
  Sprout,
  Sun,
  Trash2,
  UserRound,
  UtensilsCrossed,
  X,
} from "lucide-react";
import { api, ApiError, localDay } from "@/lib/api";
import type {
  Diary,
  Food,
  Locale,
  Meal,
  Nutrient,
  Options,
  Profile,
  Recipe,
  Summary,
} from "@/lib/types";
import { AuthView } from "./auth-view";
import { ProfileView } from "./profile-view";
import { FoodIcon, MealDrawer, RestrictionNote } from "./meal-drawer";
import {
  ErrorNotice,
  LanguageButton,
  Logo,
  Modal,
  NutrientStrip,
  SourceLink,
  Spinner,
  UIContext,
  useUI,
} from "./ui";

export function NourApp({ initialLocale }: { initialLocale: Locale }) {
  const [locale, setLocaleState] = useState(initialLocale);
  const setLocale = useCallback((next: Locale) => {
    document.documentElement.lang = next;
    document.documentElement.dir = next === "ar" ? "rtl" : "ltr";
    document.cookie = `nour_locale=${next};Path=/;Max-Age=31536000;SameSite=Lax${location.protocol === "https:" ? ";Secure" : ""}`;
    setLocaleState(next);
  }, []);
  return (
    <UIContext.Provider value={{ locale, setLocale }}>
      <Application />
    </UIContext.Provider>
  );
}

function Application() {
  const { t, locale, name, n } = useUI();
  const router = useRouter();
  const pathname = usePathname();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [options, setOptions] = useState<Options>({
    substances: [],
    conditions: [],
  });
  const [booting, setBooting] = useState(true);
  const [bootError, setBootError] = useState<unknown>(null);
  const [error, setError] = useState<unknown>(null);
  const [day, setDay] = useState("");
  const [diary, setDiary] = useState<Diary | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(false);
  const [drawer, setDrawer] = useState(false);
  const [initialRecipe, setInitialRecipe] = useState<Recipe | undefined>();
  const [menu, setMenu] = useState(false);
  const [toast, setToast] = useState("");
  const [detail, setDetail] = useState<Meal | null>(null);
  const [recipeDetail, setRecipeDetail] = useState<Recipe | null>(null);
  const [revision, setRevision] = useState(0);
  const [deleting, setDeleting] = useState(false);
  const notify = useCallback((message: string) => setToast(message), []);
  useEffect(() => {
    if (toast) {
      const timer = setTimeout(() => setToast(""), 4500);
      return () => clearTimeout(timer);
    }
  }, [toast]);
  const boot = useCallback(async () => {
    setBooting(true);
    setBootError(null);
    try {
      const current = await api<Profile>("/auth/me");
      setProfile(current);
      setDay(localDay(current.timezone));
      setOptions(await api<Options>("/catalog/options"));
    } catch (e) {
      if (!(e instanceof ApiError && e.status === 401)) setBootError(e);
    } finally {
      setBooting(false);
    }
  }, []);
  useEffect(() => {
    void boot();
    const expired = () => {
      setProfile(null);
      setDiary(null);
      setSummary(null);
      setRecipes([]);
      setOptions({ substances: [], conditions: [] });
      setDrawer(false);
      setDetail(null);
    };
    window.addEventListener("nour:expired", expired);
    return () => window.removeEventListener("nour:expired", expired);
  }, [boot]);
  useEffect(() => {
    if (!profile || !day) return;
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    Promise.all([
      api<Diary>(`/diary?day=${day}`, { signal: controller.signal }),
      api<Summary>(`/summary?day=${day}`, { signal: controller.signal }),
      api<{ items: Recipe[] }>("/recipes", { signal: controller.signal }),
    ])
      .then(([d, s, r]) => {
        setDiary(d);
        setSummary(s);
        setRecipes(r.items);
      })
      .catch((e) => {
        if (e.name !== "AbortError") setError(e);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [profile?.user.id, profile?.revision, day, revision]);
  useEffect(() => setMenu(false), [pathname]);
  async function authenticated(p: Profile) {
    setProfile(p);
    setDay(localDay(p.timezone));
    try {
      setOptions(await api<Options>("/catalog/options"));
    } catch (e) {
      setError(e);
    }
    router.push(p.onboarding_completed ? "/" : "/profile");
  }
  async function logout() {
    try {
      await api("/auth/logout", { method: "POST" });
      setProfile(null);
      setDiary(null);
      setSummary(null);
      setRecipes([]);
      router.push("/");
    } catch (e) {
      setError(e);
    }
  }
  function openMeal(recipe?: Recipe) {
    setInitialRecipe(recipe);
    setDrawer(true);
  }
  async function deleteMeal(meal: Meal) {
    if (!window.confirm(t("deleteMealConfirm"))) return;
    setDeleting(true);
    try {
      await api(`/meals/${meal.id}`, { method: "DELETE" });
      setDetail(null);
      setRevision((v) => v + 1);
      notify(t("mealDeleted"));
    } catch (e) {
      setError(e);
    } finally {
      setDeleting(false);
    }
  }
  if (booting)
    return (
      <div className="boot-screen">
        <Logo />
        <Spinner />
        <p>{t("loading")}</p>
      </div>
    );
  if (bootError)
    return (
      <div className="boot-screen">
        <Logo />
        <ErrorNotice error={bootError} />
        <button className="button primary" onClick={boot}>
          {t("retry")}
        </button>
      </div>
    );
  if (!profile) return <AuthView onSuccess={authenticated} />;
  const view =
    pathname === "/profile"
      ? "profile"
      : pathname === "/recipes"
        ? "recipes"
        : pathname === "/diary"
          ? "diary"
          : "today";
  const navigation = [
    { key: "today", href: "/", icon: LayoutDashboard },
    { key: "diary", href: "/diary", icon: BookOpen },
    { key: "recipes", href: "/recipes", icon: Sprout },
    { key: "profile", href: "/profile", icon: UserRound },
  ] as const;
  const dateText = new Intl.DateTimeFormat(
    locale === "ar" ? "ar-JO" : "en-GB",
    { weekday: "long", day: "numeric", month: "long", timeZone: "UTC" },
  ).format(new Date(`${day}T12:00:00Z`));
  return (
    <div className="app-layout">
      <a className="skip-link" href="#main">
        {locale === "ar" ? "انتقل إلى المحتوى" : "Skip to content"}
      </a>
      {menu && (
        <button
          className="mobile-scrim"
          aria-label={t("close")}
          onClick={() => setMenu(false)}
        />
      )}
      <aside className={`sidebar ${menu ? "is-open" : ""}`}>
        <div className="sidebar-brand">
          <Logo />
          <button
            className="icon-button mobile-close"
            aria-label={t("close")}
            onClick={() => setMenu(false)}
          >
            <X size={22} />
          </button>
        </div>
        <div className="sidebar-eyebrow">{t("brandLine")}</div>
        <nav
          aria-label={locale === "ar" ? "التنقل الرئيسي" : "Main navigation"}
        >
          {navigation.map(({ key, href, icon: Icon }) => (
            <Link
              href={href}
              className={`nav-link ${view === key ? "active" : ""}`}
              aria-current={view === key ? "page" : undefined}
              key={key}
            >
              <Icon size={20} />
              <span>{t(key)}</span>
              {view === key && <span className="nav-dot" />}
            </Link>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-source">
            <ShieldCheck size={23} />
            <strong>{t("sourceBacked")}</strong>
            <p>{t("sourceBackedSub")}</p>
            <span>
              USDA FoodData Central
              <ArrowUpRight size={14} />
            </span>
          </div>
          <div className="sidebar-user">
            <span className="avatar">
              {profile.user.display_name[0]?.toLocaleUpperCase()}
            </span>
            <div>
              <strong>{profile.user.display_name}</strong>
              <small>{t(profile.country === "SA" ? "saudi" : "jordan")}</small>
            </div>
            <button
              className="icon-button"
              aria-label={t("logout")}
              onClick={logout}
            >
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </aside>
      <div className="app-main">
        <header className="topbar">
          <div className="topbar-greeting">
            <button
              className="icon-button mobile-menu"
              aria-label={locale === "ar" ? "فتح القائمة" : "Open menu"}
              onClick={() => setMenu(true)}
            >
              <Menu size={22} />
            </button>
            <span>
              {t("welcome")},{" "}
              <strong>{profile.user.display_name.split(" ")[0]}</strong>{" "}
              <span className="greeting-sun">
                <Sun size={18} />
              </span>
            </span>
          </div>
          <div className="topbar-actions">
            <LanguageButton />
            <span className="topbar-divider" />
            <Link
              href="/profile"
              className="avatar small"
              aria-label={t("profile")}
            >
              {profile.user.display_name[0]?.toLocaleUpperCase()}
            </Link>
          </div>
        </header>
        <main id="main" className="content" aria-busy={loading}>
          <ErrorNotice error={error} />
          {!!error && (
            <button
              className="text-button"
              onClick={() => setRevision((v) => v + 1)}
            >
              {t("retry")}
            </button>
          )}
          {view === "profile" ? (
            <ProfileView
              key={profile.revision}
              profile={profile}
              options={options}
              onSave={(p) => {
                setProfile(p);
                notify(t("profileSaved"));
                if (!profile.onboarding_completed) router.push("/");
              }}
              onDelete={() => {
                setProfile(null);
                setDiary(null);
                setSummary(null);
                setRecipes([]);
                router.push("/");
              }}
            />
          ) : (
            <>
              <div className="page-heading">
                <div>
                  <span className="eyebrow">
                    {view === "today" ? dateText : t(view)}
                  </span>
                  <h1>
                    {t(
                      view === "today"
                        ? "overview"
                        : view === "diary"
                          ? "diaryTitle"
                          : "recipeTitle",
                    )}
                  </h1>
                  <p>
                    {t(
                      view === "today"
                        ? "overviewSub"
                        : view === "diary"
                          ? "diarySub"
                          : "recipeSub",
                    )}
                  </p>
                </div>
                <button className="button primary" onClick={() => openMeal()}>
                  <Plus size={18} />
                  {t("addMeal")}
                </button>
              </div>
              {view !== "recipes" && (
                <div className="date-control">
                  <button
                    className="icon-button"
                    aria-label={t("previousDay")}
                    onClick={() => setDay(shiftDay(day, -1))}
                  >
                    <ChevronLeft size={18} className="directional" />
                  </button>
                  <label>
                    <CalendarDays size={16} />
                    <span className="sr-only">{t("date")}</span>
                    <input
                      type="date"
                      value={day}
                      onChange={(e) => {
                        if (e.target.value) setDay(e.target.value);
                      }}
                    />
                  </label>
                  <button
                    className="icon-button"
                    aria-label={t("nextDay")}
                    onClick={() => setDay(shiftDay(day, 1))}
                  >
                    <ChevronRight size={18} className="directional" />
                  </button>
                  <button
                    className="today-button"
                    onClick={() => setDay(localDay(profile.timezone))}
                  >
                    {t("todayLabel")}
                  </button>
                </div>
              )}
              {view === "today" && (
                <>
                  <section className="welcome-banner">
                    <div>
                      <span className="eyebrow">
                        <span className="tiny-dot" />
                        {t("heroTag")}
                      </span>
                      <h2>{t("heroTitle")}</h2>
                      <p>{t("heroText")}</p>
                      <button
                        className="button banner-button"
                        onClick={() => openMeal()}
                      >
                        {t("addMeal")}
                        <ArrowUpRight size={17} />
                      </button>
                    </div>
                    <div className="banner-art" aria-hidden="true">
                      <span className="banner-orbit orbit-one" />
                      <span className="banner-orbit orbit-two" />
                      <span className="banner-leaf leaf-one">
                        <Leaf />
                      </span>
                      <span className="banner-leaf leaf-two">
                        <Leaf />
                      </span>
                      <div className="banner-plate">
                        <div className="banner-food" />
                        <span />
                        <i />
                      </div>
                      <div className="banner-floating">
                        <Check size={17} />
                        {t("sourceBacked")}
                      </div>
                    </div>
                  </section>
                  {!profile.onboarding_completed && (
                    <Link href="/profile" className="onboarding-prompt">
                      <span className="onboarding-icon">
                        <UserRound size={20} />
                      </span>
                      <div>
                        <strong>{t("profilePrompt")}</strong>
                        <p>{t("profilePromptSub")}</p>
                      </div>
                      <span>
                        {t("completeProfile")}
                        <ArrowRight className="directional" size={16} />
                      </span>
                    </Link>
                  )}
                </>
              )}
              {view !== "recipes" && (
                <>
                  <div className="stats-grid">
                    {(["calories", "protein", "carbs", "fat"] as const).map(
                      (key, index) => (
                        <StatCard
                          key={key}
                          nutrient={key}
                          value={
                            diary?.nutrition.values[key] ?? (diary ? null : "0")
                          }
                          known={diary?.nutrition.known_totals[key]}
                          goal={
                            profile[
                              key === "calories"
                                ? "calorie_target"
                                : (`${key}_target` as
                                    | "protein_target"
                                    | "carbs_target"
                                    | "fat_target")
                            ]
                          }
                          index={index}
                        />
                      ),
                    )}
                  </div>
                  {diary && !diary.nutrition.complete && (
                    <div className="note amber">{t("incomplete")}</div>
                  )}
                </>
              )}
              {view === "today" && (
                <div className="dashboard-grid">
                  <section className="panel rhythm-card">
                    <div className="section-heading">
                      <div>
                        <h2>{t("rhythm")}</h2>
                        <p>{t("rhythmSub")}</p>
                      </div>
                      <span className="chart-legend">
                        <span />
                        {t("energyIntake")}
                      </span>
                    </div>
                    <WeeklyChart
                      summary={summary}
                      selected={day}
                      onSelect={setDay}
                    />
                  </section>
                  <section className="panel source-card">
                    <div className="source-card-top">
                      <span>
                        <ShieldCheck size={24} />
                      </span>
                      <span className="verified-dots">
                        <i />
                        <i />
                        <i />
                      </span>
                    </div>
                    <h2>{t("sourceBacked")}</h2>
                    <p>{t("sourceBackedSub")}</p>
                    <button className="text-button" onClick={() => openMeal()}>
                      {t("browseFoods")}
                      <ArrowUpRight size={17} />
                    </button>
                    <div className="source-wordmark">
                      <Leaf size={18} />
                      USDA <span>FoodData Central</span>
                    </div>
                  </section>
                </div>
              )}
              {view !== "recipes" && (
                <section className="panel diary-panel">
                  <div className="section-heading">
                    <div>
                      <h2>{t(view === "diary" ? "diary" : "mealSection")}</h2>
                      <p>
                        {dateText} <span className="dot">·</span>{" "}
                        {n(diary?.meals.length || 0)} {t("entries")}
                      </p>
                    </div>
                    {view === "today" ? (
                      <Link className="text-button" href="/diary">
                        {t("viewDiary")}
                        <ArrowRight className="directional" size={16} />
                      </Link>
                    ) : (
                      <button
                        className="text-button"
                        onClick={() => openMeal()}
                      >
                        <Plus size={16} />
                        {t("addMeal")}
                      </button>
                    )}
                  </div>
                  {!diary?.meals.length ? (
                    <div className="empty-diary">
                      <span>
                        <UtensilsCrossed size={27} />
                      </span>
                      <h3>{t("emptyMeals")}</h3>
                      <p>{t("emptyMealsSub")}</p>
                      <button
                        className="button secondary"
                        onClick={() => openMeal()}
                      >
                        <Plus size={17} />
                        {t("addMeal")}
                      </button>
                    </div>
                  ) : (
                    <div className="meal-list">
                      {diary.meals.map((meal) => (
                        <button
                          className="meal-row"
                          key={meal.id}
                          onClick={() => setDetail(meal)}
                        >
                          <span className={`meal-icon ${meal.meal_type}`}>
                            <UtensilsCrossed size={21} />
                          </span>
                          <div className="meal-row-name">
                            <strong>{meal.title}</strong>
                            <span>
                              {t(meal.meal_type as "lunch")}
                              <span className="dot">·</span>
                              {n(meal.items.length)} {t("foodCount")}
                            </span>
                          </div>
                          <div className="meal-row-macros">
                            <span>
                              P{" "}
                              <b>
                                {meal.nutrition.values.protein === null
                                  ? "—"
                                  : n(meal.nutrition.values.protein, 1)}
                              </b>
                            </span>
                            <span>
                              C{" "}
                              <b>
                                {meal.nutrition.values.carbs === null
                                  ? "—"
                                  : n(meal.nutrition.values.carbs, 1)}
                              </b>
                            </span>
                            <span>
                              F{" "}
                              <b>
                                {meal.nutrition.values.fat === null
                                  ? "—"
                                  : n(meal.nutrition.values.fat, 1)}
                              </b>
                            </span>
                          </div>
                          <div className="meal-row-energy">
                            <strong>
                              {meal.nutrition.values.calories === null
                                ? "—"
                                : n(meal.nutrition.values.calories)}
                            </strong>
                            <small>{t("kcal")}</small>
                          </div>
                          <ChevronRight size={18} className="directional" />
                        </button>
                      ))}
                    </div>
                  )}
                </section>
              )}
              {view === "recipes" && (
                <>
                  <div className="note recipe-notice">
                    <Leaf size={19} />
                    {t("sampleNote")}
                  </div>
                  <div className="recipe-grid">
                    {recipes.map((recipe, index) => (
                      <article className="recipe-card panel" key={recipe.id}>
                        <div
                          className={`recipe-art recipe-art-${index}`}
                          aria-hidden="true"
                        >
                          <div className="recipe-bowl">
                            <span />
                            <i />
                            <b />
                          </div>
                          <span className="recipe-art-leaf">
                            <Leaf size={48} />
                          </span>
                          <span className="recipe-index">0{index + 1}</span>
                        </div>
                        <div className="recipe-card-body">
                          <span className="eyebrow">{t("sampleRecipe")}</span>
                          <h2>{name(recipe)}</h2>
                          <div className="recipe-meta">
                            <span>
                              {n(recipe.serving_grams)} {t("g")}{" "}
                              <span className="dot">·</span> {t("serving")}
                            </span>
                            <strong>
                              {recipe.nutrients.calories === null
                                ? "—"
                                : n(recipe.nutrients.calories)}{" "}
                              <small>{t("kcal")}</small>
                            </strong>
                          </div>
                          <NutrientStrip values={recipe.nutrients} />
                          <button
                            className="button secondary"
                            onClick={() => setRecipeDetail(recipe)}
                          >
                            {t("viewRecipe")}
                            <ArrowUpRight size={17} />
                          </button>
                        </div>
                      </article>
                    ))}
                  </div>
                </>
              )}
            </>
          )}
          <footer className="app-footer">
            <span>
              <Sprout size={15} />
              {t("brandLine")}
            </span>
            <span>{t("authFeature3")}</span>
          </footer>
        </main>
      </div>
      {drawer && (
        <MealDrawer
          key={initialRecipe?.id || "manual"}
          open={drawer}
          onClose={() => setDrawer(false)}
          onSaved={() => {
            setDrawer(false);
            setRevision((v) => v + 1);
            notify(t("mealSaved"));
          }}
          profile={profile}
          day={day}
          initialRecipe={initialRecipe}
        />
      )}
      <Modal
        open={!!detail}
        onClose={() => setDetail(null)}
        title={detail?.title || ""}
        description={t("sourceDetails")}
        className="details-modal"
        busy={deleting}
      >
        <div className="modal-body stack">
          {detail && (
            <>
              <NutrientStrip values={detail.nutrition.values} />
              <RestrictionNote status={detail.restrictions.status} />
              <div className="snapshot-list">
                {detail.items.map((item, index) => (
                  <div key={index} className="snapshot-item">
                    <div>
                      <strong>{name(item.source)}</strong>
                      <span>
                        {n(item.grams, 1)} {t("g")} ·{" "}
                        {t(
                          item.evidence === "weighed" ? "measured" : "entered",
                        )}
                      </span>
                    </div>
                    {item.type === "food" ? (
                      <SourceLink url={(item.source as Food).source.url}>
                        FDC {(item.source as Food).source.external_id}
                      </SourceLink>
                    ) : (
                      <span className="tag">
                        {t("sampleRecipe")} · v{(item.source as Recipe).version}
                      </span>
                    )}
                  </div>
                ))}
              </div>
              <p className="muted small-text">
                {t("inputSnapshot")} · {t("sourceVersion")}{" "}
                {detail.calculation_version}
              </p>
              <button
                className="text-button danger"
                onClick={() => deleteMeal(detail)}
                disabled={deleting}
              >
                {deleting ? <Spinner /> : <Trash2 size={16} />} {t("delete")}
              </button>
            </>
          )}
        </div>
      </Modal>
      <Modal
        open={!!recipeDetail}
        onClose={() => setRecipeDetail(null)}
        title={recipeDetail ? name(recipeDetail) : ""}
        description={t("sampleNote")}
        className="details-modal"
      >
        <div className="modal-body stack">
          {recipeDetail && (
            <>
              <NutrientStrip values={recipeDetail.nutrients} />
              <div className="recipe-yield">
                <span>
                  {t("serving")}{" "}
                  <strong>
                    {n(recipeDetail.serving_grams)} {t("g")}
                  </strong>
                </span>
                <span>
                  {t("batchYield")}{" "}
                  <strong>
                    {n(recipeDetail.yield_grams)} {t("g")}
                  </strong>
                </span>
              </div>
              <h3>{t("ingredients")}</h3>
              <div className="snapshot-list">
                {recipeDetail.ingredients.map((i, index) => (
                  <div className="snapshot-item" key={index}>
                    <div>
                      <strong>{name(i.food)}</strong>
                      <span>
                        {n(i.grams)} {t("g")}
                      </span>
                    </div>
                    <SourceLink url={i.food.source.url}>
                      FDC {i.food.source.external_id}
                    </SourceLink>
                  </div>
                ))}
              </div>
              <p className="muted small-text">{t("sourceNote")}</p>
              <h3>{t("method")}</h3>
              <p className="section-description">
                {locale === "ar"
                  ? recipeDetail.method_ar
                  : recipeDetail.method_en}
              </p>
              <button
                className="button primary"
                onClick={() => {
                  const r = recipeDetail;
                  setRecipeDetail(null);
                  openMeal(r);
                }}
              >
                <Plus size={17} />
                {t("logPortion")}
              </button>
            </>
          )}
        </div>
      </Modal>
      {toast && (
        <div className="toast" role="status">
          <Check size={18} />
          {toast}
          <button
            className="icon-button"
            aria-label={t("close")}
            onClick={() => setToast("")}
          >
            <X size={15} />
          </button>
        </div>
      )}
    </div>
  );
}
function shiftDay(day: string, amount: number) {
  const date = new Date(`${day}T12:00:00Z`);
  date.setUTCDate(date.getUTCDate() + amount);
  return date.toISOString().slice(0, 10);
}
function StatCard({
  nutrient,
  value,
  known,
  goal,
  index,
}: {
  nutrient: Nutrient;
  value: string | null;
  known?: string | null;
  goal: string | null;
  index: number;
}) {
  const { t, n } = useUI();
  const numeric = Number(value ?? known ?? 0),
    target = Number(goal || 0),
    progress = target > 0 ? Math.min(100, (numeric / target) * 100) : 0;
  return (
    <section className={`stat-card stat-${index}`}>
      <div className="stat-top">
        <span className="stat-icon">
          {index === 0 ? (
            <Flame size={19} />
          ) : (
            <span>{["", "P", "C", "F"][index]}</span>
          )}
        </span>
        <span>{t(nutrient)}</span>
        {index === 0 && target > 0 && (
          <span className="stat-percent">{n(progress)}%</span>
        )}
      </div>
      <div className="stat-value">
        <strong>
          {value === null ? "—" : n(value, nutrient === "calories" ? 0 : 1)}
        </strong>
        <span>{t(nutrient === "calories" ? "kcal" : "g")}</span>
      </div>
      <div className="stat-track">
        <span style={{ width: `${progress}%` }} />
      </div>
      <p>
        {value === null ? (
          <span>
            {t("availableTotal")}: {n(known)}{" "}
            {t(nutrient === "calories" ? "kcal" : "g")}
          </span>
        ) : goal ? (
          <>
            <strong>
              {n(
                Math.max(0, target - numeric),
                nutrient === "calories" ? 0 : 1,
              )}
            </strong>{" "}
            {t("remaining")}{" "}
            <span>
              · {n(goal)} {t("target")}
            </span>
          </>
        ) : (
          <Link href="/profile">
            {t("noTarget")}
            <ArrowUpRight size={13} />
          </Link>
        )}
      </p>
    </section>
  );
}
function WeeklyChart({
  summary,
  selected,
  onSelect,
}: {
  summary: Summary | null;
  selected: string;
  onSelect: (day: string) => void;
}) {
  const { t, locale, n } = useUI();
  const days = summary?.days || [];
  const max = Math.max(
    1,
    ...days.map((d) => Number(d.nutrition.known_totals.calories)),
  );
  const any = days.some((d) => d.meal_count > 0);
  return (
    <div className="weekly-chart">
      <div className="chart-scale">
        <span>{n(max)}</span>
        <span>{n(max / 2)}</span>
        <span>{n(0)}</span>
      </div>
      <div className="chart-plot">
        <div className="chart-grid">
          <i />
          <i />
          <i />
        </div>
        <div className="chart-bars">
          {days.map((d) => (
            <button
              key={d.date}
              className={`chart-day ${d.date === selected ? "selected" : ""}`}
              onClick={() => onSelect(d.date)}
              aria-label={`${d.date}: ${n(d.nutrition.known_totals.calories)} ${t("kcal")}${d.nutrition.complete ? "" : ` · ${t("incomplete")}`}`}
            >
              <span className="bar-space">
                <span
                  className={`chart-bar ${d.meal_count ? "has-data" : ""}`}
                  style={{
                    height: `${Math.max(3, (Number(d.nutrition.known_totals.calories) / max) * 100)}%`,
                  }}
                />
              </span>
              <span>
                {new Intl.DateTimeFormat(locale === "ar" ? "ar-JO" : "en-GB", {
                  weekday: "short",
                  timeZone: "UTC",
                }).format(new Date(`${d.date}T12:00:00Z`))}
              </span>
            </button>
          ))}
        </div>
        {!any && <p className="chart-empty">{t("noChart")}</p>}
      </div>
    </div>
  );
}
