export type Locale = "en" | "ar";
export type Nutrient =
  "calories" | "protein" | "carbs" | "fat" | "fiber" | "sodium";
export type Values = Record<Nutrient, string | null>;
export type Nutrition = {
  values: Values;
  known_totals: Values;
  missing: string[];
  complete: boolean;
};
export type Restriction = {
  substance_id: string;
  kind: "allergy" | "intolerance" | "dislike";
  confirmed?: boolean;
};
export type Check = {
  status: "conflict" | "unknown" | "no_recorded_conflict";
  matches: Restriction[];
  cross_contact: string;
  recommendation_eligible: boolean;
};
export type Profile = {
  user: { id: string; email: string; display_name: string; role: string };
  locale: Locale;
  country: "JO" | "SA";
  timezone: string;
  units: "metric" | "imperial";
  goal: string;
  target_origin: string;
  calorie_target: string | null;
  protein_target: string | null;
  carbs_target: string | null;
  fat_target: string | null;
  allergy_status: "unknown" | "none" | "recorded";
  preferences: string[];
  revision: number;
  onboarding_completed: boolean;
  restrictions: Restriction[];
  conditions: string[];
};
export type Food = {
  id: string;
  name_en: string;
  name_ar: string;
  category: string;
  preparation: string;
  basis_grams: string;
  nutrients: Values;
  source: {
    name: string;
    url: string;
    data_type: string;
    source_date: string;
    external_id: string;
    version: number;
  };
  ingredient_substances: string[];
  ingredient_coverage: string;
};
export type Recipe = {
  id: string;
  recipe_id: string;
  name_en: string;
  name_ar: string;
  version: number;
  is_sample: boolean;
  yield_grams: string;
  serving_grams: string;
  method_en: string;
  method_ar: string;
  review_status: string;
  nutrients: Values;
  ingredients: { food: Food; grams: string }[];
  ingredient_substances: string[];
  ingredient_coverage: string;
};
export type ItemSnapshot = {
  type: "food" | "recipe";
  source: Food | Recipe;
  grams: string;
  evidence: string;
  nutrients: Values;
};
export type Meal = {
  id: string;
  title: string;
  meal_type: string;
  status: string;
  consumed_at: string;
  confirmed_at: string | null;
  nutrition: Nutrition;
  restrictions: Check;
  calculation_version: string;
  items: ItemSnapshot[];
};
export type Diary = {
  date: string;
  timezone: string;
  nutrition: Nutrition;
  meals: Meal[];
};
export type Summary = {
  days: { date: string; nutrition: Nutrition; meal_count: number }[];
};
export type Options = {
  substances: { id: string; name_en: string; name_ar: string }[];
  conditions: {
    id: string;
    name_en: string;
    name_ar: string;
    module_status: string;
  }[];
};
export type Selection = {
  key: string;
  type: "food" | "recipe";
  item: Food | Recipe;
  grams: string;
  evidence: "weighed" | "user_entered";
};
export type Preview = {
  nutrition: Nutrition;
  items: ItemSnapshot[];
  restrictions: Check;
  calculation_version: string;
};
