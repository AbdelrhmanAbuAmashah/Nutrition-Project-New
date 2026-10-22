import { test, expect } from "@playwright/test";

test.afterEach(async ({ page }, testInfo) => {
  const email = testInfo.annotations.find(
    (item) => item.type === "qa-account",
  )?.description;
  if (!email) return;
  const login = await page.request.post("/api/v1/auth/login", {
    data: { email, password: "TestPassword!234" },
  });
  if (login.status() !== 200) return; // The successful UI flow already deletes its account.
  const cookies = await page.context().cookies();
  const csrf =
    cookies.find((cookie) => cookie.name === "nour_csrf")?.value || "";
  const removed = await page.request.delete("/api/v1/account", {
    data: { password: "TestPassword!234" },
    headers: { "X-CSRF-Token": csrf },
  });
  expect(removed.status()).toBe(204);
});

test("source-backed diary persists, works in Arabic, and protects the session", async ({
  page,
}, testInfo) => {
  const email = `nour-qa-${Date.now()}-${testInfo.project.name}@example.com`;
  testInfo.annotations.push({ type: "qa-account", description: email });
  const arabic = testInfo.project.name.endsWith("-ar");
  const mobile = testInfo.project.name.startsWith("mobile");
  await page.goto("/");
  if (arabic) await page.getByRole("button", { name: "العربية" }).click();
  await expect(page.locator("html")).toHaveAttribute(
    "dir",
    arabic ? "rtl" : "ltr",
  );
  await page
    .getByRole("textbox", { name: arabic ? "اسمك" : "Your name", exact: true })
    .fill(arabic ? "أمل" : "Amal");
  await page
    .getByRole("textbox", {
      name: arabic ? "البريد الإلكتروني" : "Email address",
      exact: true,
    })
    .fill(email);
  await page
    .getByLabel(arabic ? "كلمة المرور" : "Password", { exact: true })
    .fill("TestPassword!234");
  await page.getByRole("checkbox").check();
  await page
    .getByRole("button", {
      name: arabic ? "إنشاء حساب" : "Create account",
      exact: true,
    })
    .last()
    .click();
  await expect(
    page.getByRole("heading", {
      name: arabic ? "تفاصيل تشبهك." : "A little more you.",
    }),
  ).toBeVisible();
  await page
    .getByRole("combobox", {
      name: arabic ? "معلومات الحساسية الغذائية" : "Food allergy information",
      exact: true,
    })
    .selectOption("none");
  await page
    .getByRole("button", {
      name: arabic ? "حفظ وبدء يوميّاتي" : "Save & start my diary",
      exact: true,
    })
    .click();
  await expect(
    page.getByRole("heading", {
      name: arabic ? "نظرة على يومك" : "Your daily overview",
    }),
  ).toBeVisible();
  await page
    .getByRole("button", {
      name: arabic ? "تسجيل وجبة" : "Log a meal",
      exact: true,
    })
    .first()
    .click();
  const dialog = page.getByRole("dialog");
  await expect(dialog).toBeVisible();
  await dialog
    .getByRole("textbox", {
      name: arabic
        ? "ابحث عن الأطعمة بالعربية أو الإنجليزية…"
        : "Search foods in English or Arabic…",
    })
    .fill(arabic ? "أرز" : "rice");
  await dialog
    .getByRole("button", {
      name: arabic ? "إضافة أرز أبيض · مطبوخ" : "Add White rice · cooked",
      exact: true,
    })
    .click();
  await dialog
    .getByRole("textbox", {
      name: arabic ? "الكمية أرز أبيض · مطبوخ" : "Quantity White rice · cooked",
      exact: true,
    })
    .fill(arabic ? "١٥٠" : "150");
  await dialog
    .getByRole("textbox", {
      name: arabic ? "اسم الوجبة" : "Meal name",
      exact: true,
    })
    .fill("QA Lunch");
  const save = dialog.getByRole("button", {
    name: arabic ? "تأكيد الوجبة وحفظها" : "Confirm & save meal",
    exact: true,
  });
  await expect(save).toBeEnabled();
  await save.click();
  await expect(dialog).toBeHidden();
  await expect(page.getByRole("button", { name: /QA Lunch/ })).toBeVisible();
  await page.reload();
  await expect(page.getByRole("button", { name: /QA Lunch/ })).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth + 1,
    ),
  ).toBeTruthy();
  await page.screenshot({
    path: `test-results/${testInfo.project.name}-dashboard.png`,
    fullPage: true,
  });
  await page.getByRole("button", { name: /QA Lunch/ }).click();
  await expect(page.getByRole("link", { name: "FDC 168878" })).toBeVisible();
  await page
    .getByRole("dialog")
    .getByRole("button", { name: arabic ? "إغلاق" : "Close", exact: true })
    .click();
  const cookies = await page.context().cookies();
  expect(cookies.find((c) => c.name === "nour_access")?.httpOnly).toBeTruthy();
  expect(
    await page.evaluate(() => document.cookie.includes("nour_access=")),
  ).toBeFalsy();
  const unauthorized = await page.request.post("/api/v1/auth/logout");
  expect(unauthorized.status()).toBe(403);
  if (mobile)
    await page
      .getByRole("button", { name: arabic ? "فتح القائمة" : "Open menu" })
      .click();
  await page
    .getByRole("link", {
      name: arabic ? "مطبخنا المحلي" : "The local kitchen",
      exact: true,
    })
    .click();
  await expect(
    page.getByRole("heading", {
      name: arabic ? "طبق مجدّرة" : "Mujaddara bowl",
      exact: true,
    }),
  ).toBeVisible();
  await page
    .getByRole("button", {
      name: arabic ? "عرض الوصفة" : "View recipe",
      exact: true,
    })
    .first()
    .click();
  await expect(
    page.getByRole("dialog").getByRole("heading", {
      name: arabic ? "المكوّنات" : "Ingredients",
      exact: true,
    }),
  ).toBeVisible();
  await page
    .getByRole("dialog")
    .getByRole("button", { name: arabic ? "إغلاق" : "Close", exact: true })
    .click();
  if (mobile)
    await page
      .getByRole("button", { name: arabic ? "فتح القائمة" : "Open menu" })
      .click();
  await page
    .getByRole("link", {
      name: arabic ? "ملفي الشخصي" : "My profile",
      exact: true,
    })
    .first()
    .click();
  await page
    .getByRole("button", {
      name: arabic ? "حذف حسابي" : "Delete my account",
      exact: true,
    })
    .click();
  const deleteDialog = page.getByRole("dialog");
  await deleteDialog
    .getByLabel(arabic ? "كلمة المرور" : "Password", { exact: true })
    .fill("TestPassword!234");
  await deleteDialog
    .getByRole("button", {
      name: arabic ? "حذف حسابي" : "Delete my account",
      exact: true,
    })
    .click();
  await expect(
    page.getByRole("heading", {
      name: arabic
        ? "مساحة ليومٍ أفضل تغذية."
        : "Make room for a nourished day.",
    }),
  ).toBeVisible();
});
