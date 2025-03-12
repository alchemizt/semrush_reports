const db = require("../database");

describe("SQLite Database Tests", () => {
  beforeAll(() => {
    db.exec("DELETE FROM reports"); // Clean table before tests
  });

  test("Insert data into SQLite", () => {
    const stmt = db.prepare("INSERT INTO reports (keyword, ranking) VALUES (?, ?)");
    stmt.run("jest_test", 2);

    const row = db.prepare("SELECT * FROM reports WHERE keyword = ?").get("jest_test");

    expect(row).not.toBeNull();
    expect(row.ranking).toBe(2);
  });

  afterAll(() => {
    db.close();
  });
});
