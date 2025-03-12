
let db;

beforeAll(async () => {
  db = new Database("semrush_data.db");
  db.exec("DELETE FROM reports"); // Clean table before tests

  driver = await new Builder()
    .forBrowser("chrome")
    .setChromeOptions(
      new (require("selenium-webdriver/chrome").Options)()
        .headless()  // Run in headless mode for CI/CD
        .windowSize({ width: 1920, height: 1080 })
    )
    .build();
});

afterAll(async () => {
  await driver.quit();
  db.close();
});

test("Verify SEMrush Title", async () => {
  await driver.get("https://www.semrush.com");
  const title = await driver.getTitle();
  expect(title.toLowerCase()).toContain("semrush");
});

test("Insert SEMrush Keyword Data into SQLite", async () => {
  const keyword = "SEO Test";
  const ranking = 1;

  const stmt = db.prepare("INSERT INTO reports (keyword, ranking) VALUES (?, ?)");
  stmt.run(keyword, ranking);

  const row = db.prepare("SELECT * FROM reports WHERE keyword = ?").get(keyword);
  expect(row).not.toBeNull();
  expect(row.ranking).toBe(1);
}); 