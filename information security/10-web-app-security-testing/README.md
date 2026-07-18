# 10 — Web Application Security Testing

## Objective
Identify and understand common web vulnerabilities using OWASP's
intentionally-vulnerable practice application (DVWA — Damn Vulnerable Web
App), running only inside the isolated lab.

## Concepts (OWASP Top 10 items covered)
- **SQL Injection (SQLi):** attacker input is concatenated directly into a
  database query, letting them alter its logic (e.g., bypass a login).
- **Cross-Site Scripting (XSS):** attacker-supplied script is reflected/
  stored and executed in another user's browser.
- **Broken Authentication:** weak session/login handling that lets an
  attacker hijack or bypass authentication.
- **Why input validation & parameterized queries matter:** both SQLi and XSS
  are fixed at the root by never trusting user input and never building
  queries/HTML via string concatenation.

## Tools Used
DVWA (target app), Burp Suite (intercepting proxy), browser dev tools

## Steps Performed
1. Deployed DVWA on the Metasploitable2/lab VM, set security level to "low"
   for the learning exercise.
2. **SQL Injection test** — in the DVWA "SQL Injection" module, submitted
   `' OR '1'='1` into the ID field.
3. **XSS test** — in the "XSS (Reflected)" module, submitted
   `<script>alert('test')</script>` into the input field.
4. Used Burp Suite in intercept mode to view/modify the raw HTTP request
   before it reached the server, to see exactly what the app receives.

## Sample Output / Observations
The SQLi payload `' OR '1'='1` returned **all** rows in the user table
instead of just one — because the injected `OR '1'='1'` makes the query's
WHERE clause always true. This demonstrates why raw string concatenation
into SQL queries is dangerous, and why parameterized queries (prepared
statements) are the standard fix.

The XSS payload caused a JavaScript alert box to execute in the browser,
confirming the application reflects unescaped user input directly into the
page — the fix is output-encoding any user-controlled data before rendering
it as HTML.

Burp Suite's intercepted request showed the exact GET parameters being sent,
useful for understanding how the payload reaches the vulnerable code path.

## Conclusion
Both vulnerabilities come from the same root cause — **trusting user input**
— and both are prevented with the same principle: validate/sanitize input,
and never mix user data with code (SQL or HTML) without escaping it.
