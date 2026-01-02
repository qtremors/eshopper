# Project Status: ⛔ Archived

> **Note:** This project is **no longer maintained**. It served as a learning sandbox for Django integration.
> Please refer to **[Amanzon](https://github.com/qtremors/amanzon)** for a codebase that demonstrates modern best practices.

---

# 🛑 Known Issues & Review Findings
*The following issues were identified during a deep review on 2025-12-19 and are the primary reasons for archiving this project. They will not be fixed.*

## 🔴 CRITICAL SECURITY ISSUES

### 1. Plaintext Password Storage
- **File:** `shopapp/models.py`, `shopapp/views.py`
- **Issue:** User passwords are stored and compared as plaintext.
- **Impact:** Any database breach exposes all user passwords immediately.

### 2. Hardcoded Razorpay API Keys
- **File:** `shopapp/views.py`
- **Issue:** Razorpay API keys are hardcoded directly in the checkout view.
- **Impact:** API keys are exposed in version control.

### 3. Different Razorpay Key in Template
- **File:** `shopapp/templates/checkout.html`
- **Issue:** A different Razorpay key (`rzp_test_bilBagOBVTi4lE`) is used in the template than in views.
- **Impact:** Payment processing inconsistency; may cause payment failures.

### 4. Empty SECRET_KEY
- **File:** `shopping/settings.py`
- **Issue:** `SECRET_KEY = ''` is empty.
- **Impact:** Django security relies on this; sessions and CSRF protection compromised.

### 5. OTP Never Cleared
- **File:** `shopapp/views.py`
- **Issue:** After password reset, OTP is commented out (`# user.otp = None`).
- **Impact:** OTP remains valid indefinitely, allowing reuse for password resets.

---

## 🟠 BUGS & LOGIC ERRORS

### 6. Bug in confirm_password View
- **File:** `shopapp/views.py`
- **Issue:** Uses `User.objects.filter()` which returns a QuerySet, then attempts to access `.otp` on it, which causes a crash.

### 7. No Error Handling in inc/dec/del Product Views
- **File:** `shopapp/views.py`
- **Issue:** Uses `.get(id=id)` without exception handling; will crash if ID doesn't exist.

### 8. Duplicate add_review URL Pattern
- **File:** `shopapp/urls.py`
- **Issue:** Two patterns with same name `add_review`, causing URL reverse confusion.

### 9. Cancel Order Deletes Without Authorization Check
- **File:** `shopapp/views.py`
- **Issue:** Any logged-in user could potentially cancel any order by ID.

---

## 🟡 DEAD CODE & UNUSED FILES

### 10. Unused forms.py
- **File:** `shopapp/forms.py`
- **Issue:** Contains `RegistrationForm` with fields (`name`, `address`, `phone`) that don't exist in the User model. Form is never used.

### 11. Debug Print Statements
- **File:** `shopapp/views.py`
- **Issue:** Multiple `print()` statements for debugging left in production code.

### 12. Empty tests.py
- **File:** `shopapp/tests.py`
- **Issue:** No tests written.

### 13. Commented-Out Code in Templates
- **Files:** Multiple templates (`index.html`, `login.html`, etc.) contain large blocks of commented-out HTML.

---

## 🔵 ARCHITECTURE & MODULARITY ISSUES

### 14. Custom User Model Instead of Django Auth
- **File:** `shopapp/models.py`
- **Issue:** Project uses custom `User` model without extending `AbstractUser`.
- **Impact:** Loses Django's built-in auth features, password hashing, permissions.

### 15. Session-Based Auth Without Django Auth
- **File:** `shopapp/views.py`
- **Issue:** Manual session management (`request.session['email']`) instead of Django auth.

### 16. No requirements.txt
- **Issue:** No dependency file found in project.

### 17. No Base Template Usage
- **Files:** Multiple templates.
- **Issue:** Templates duplicate entire HTML structure instead of using template inheritance.

### 18. Image Upload Path Typo & Inconsistency
- **File:** `shopapp/models.py`
- **Issue:** Product image uploads to `"ststic"` (typo). Models use different upload paths inconsistent with standard practices.

### 19. Media Configuration Commented Out
- **File:** `shopping/settings.py`
- **Issue:** `MEDIA_URL` and `MEDIA_ROOT` are commented out, breaking media serving.

---

## 🟣 INCOMPLETE FEATURES & UI ISSUES

### 20. Non-Functional UI Elements
- **Newsletter:** Forms post to empty action.
- **Sorting:** Dropdown in shop page is non-functional.
- **Variants:** Size/Color selectors are static HTML.
- **Search:** Header search form has empty action.
- **Links:** Social media and Help links are empty.

### 21. UX Gaps
- **Logout:** Doesn't redirect properly (renders literal template).
- **Feedback:** Missing user feedback messages for many actions.
- **Hardcoded Data:** Product counts and "Trendy Products" sections are hardcoded static HTML.
- **404:** No custom 404 page.

---

## 🔧 TECHNICAL DEBT

### 22. Hardcoded Shipping Cost
- **Issue:** Shipping cost is hardcoded as `50` in multiple places.

### 23. Basic Admin
- **Issue:** Models registered without any customization.

### 24. Performance
- **Issue:** N+1 Query issues in loops (shop, cart).
- **Issue:** No caching.
- **Issue:** Static files included via direct script tags instead of `{% static %}`.
