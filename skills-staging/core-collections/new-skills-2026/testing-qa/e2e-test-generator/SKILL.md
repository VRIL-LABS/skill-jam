---
name: e2e-test-generator
description: Generate end-to-end tests with Playwright, Cypress, or Selenium — user journey testing, cross-browser validation, and automated testing. Use when testing complete user workflows, validating features across browsers, creating regression test suites, implementing CI/CD testing, or ensuring application quality before releases.
---

# e2e-test-generator

Create comprehensive end-to-end tests for web applications with modern testing frameworks.

## When to Use

Invoke this skill when you need to:
- **Test complete user workflows** from start to finish
- **Validate features** across different browsers and devices
- **Create regression test suites** for critical paths
- **Automate testing** in CI/CD pipelines
- **Generate test code** from user stories or requirements
- **Debug failing tests** and improve test reliability
- **Implement visual regression** testing
- **Test** single-page applications (SPAs) or complex UIs

## Quick Start

### Playwright Example

```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://example.com');
  });

  test('successful login flow', async ({ page }) => {
    // Navigate to login page
    await page.click('text=Sign In');
    
    // Fill in credentials
    await page.fill('input[name="email"]', 'user@example.com');
    await page.fill('input[name="password"]', 'SecurePassword123!');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Verify redirect to dashboard
    await expect(page).toHaveURL(/.*dashboard/);
    
    // Verify user is logged in
    await expect(page.locator('text=Welcome back')).toBeVisible();
    
    // Verify user menu contains email
    await expect(page.locator('[data-testid="user-menu"]')).toContainText('user@example.com');
  });

  test('login with invalid credentials', async ({ page }) => {
    await page.click('text=Sign In');
    await page.fill('input[name="email"]', 'wrong@example.com');
    await page.fill('input[name="password"]', 'WrongPassword');
    await page.click('button[type="submit"]');
    
    // Verify error message
    await expect(page.locator('.error-message')).toContainText('Invalid credentials');
    
    // Verify still on login page
    await expect(page).toHaveURL(/.*login/);
  });

  test('password reset flow', async ({ page }) => {
    await page.click('text=Sign In');
    await page.click('text=Forgot password?');
    
    await page.fill('input[name="email"]', 'user@example.com');
    await page.click('button:has-text("Send Reset Link")');
    
    await expect(page.locator('.success-message'))
      .toContainText('Password reset link sent');
  });
});
```

### Cypress Example

```typescript
// cypress/e2e/checkout.cy.ts
describe('E-commerce Checkout', () => {
  beforeEach(() => {
    cy.visit('/');
    // Login before each test
    cy.login('customer@example.com', 'password123');
  });

  it('completes full checkout flow', () => {
    // Add items to cart
    cy.get('[data-testid="product-1"]').click();
    cy.get('button:contains("Add to Cart")').click();
    cy.get('.notification').should('contain', 'Added to cart');
    
    // Go to cart
    cy.get('[data-testid="cart-icon"]').click();
    cy.url().should('include', '/cart');
    
    // Verify cart contents
    cy.get('[data-testid="cart-items"]').should('have.length', 1);
    cy.get('[data-testid="cart-total"]').should('contain', '$29.99');
    
    // Proceed to checkout
    cy.get('button:contains("Checkout")').click();
    
    // Fill shipping information
    cy.get('input[name="fullName"]').type('John Doe');
    cy.get('input[name="address"]').type('123 Main St');
    cy.get('input[name="city"]').type('New York');
    cy.get('select[name="state"]').select('NY');
    cy.get('input[name="zipCode"]').type('10001');
    
    // Continue to payment
    cy.get('button:contains("Continue to Payment")').click();
    
    // Fill payment information (using test card)
    cy.get('iframe[name="card-frame"]').then($iframe => {
      const $body = $iframe.contents().find('body');
      cy.wrap($body)
        .find('input[name="cardNumber"]')
        .type('4242424242424242');
      cy.wrap($body)
        .find('input[name="cardExpiry"]')
        .type('1225');
      cy.wrap($body)
        .find('input[name="cardCvc"]')
        .type('123');
    });
    
    // Place order
    cy.get('button:contains("Place Order")').click();
    
    // Verify order confirmation
    cy.url().should('include', '/order-confirmation');
    cy.get('h1').should('contain', 'Order Confirmed');
    cy.get('[data-testid="order-number"]').should('exist');
    
    // Verify email notification sent
    cy.task('checkEmail', {
      to: 'customer@example.com',
      subject: 'Order Confirmation'
    }).should('exist');
  });

  it('applies discount code', () => {
    // Add item to cart
    cy.get('[data-testid="product-1"]').click();
    cy.get('button:contains("Add to Cart")').click();
    cy.get('[data-testid="cart-icon"]').click();
    
    // Apply discount code
    cy.get('input[name="discountCode"]').type('SAVE20');
    cy.get('button:contains("Apply")').click();
    
    // Verify discount applied
    cy.get('[data-testid="discount-amount"]').should('contain', '-$6.00');
    cy.get('[data-testid="cart-total"]').should('contain', '$23.99');
  });

  it('handles out of stock items', () => {
    cy.get('[data-testid="product-out-of-stock"]').click();
    
    cy.get('button:contains("Add to Cart")').should('be.disabled');
    cy.get('.stock-status').should('contain', 'Out of Stock');
    
    // Verify notify me option
    cy.get('button:contains("Notify Me")').should('be.visible');
  });
});

// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="password"]').type(password);
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

## Common Scenarios

### Scenario 1: API Mocking and Stubbing

```typescript
// Playwright with API mocking
import { test, expect } from '@playwright/test';

test('load users with mocked API', async ({ page }) => {
  // Intercept API requests and return mock data
  await page.route('**/api/users', route => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Alice', email: 'alice@example.com' },
        { id: 2, name: 'Bob', email: 'bob@example.com' }
      ])
    });
  });
  
  await page.goto('/users');
  
  // Verify mocked data is displayed
  await expect(page.locator('[data-testid="user-1"]')).toContainText('Alice');
  await expect(page.locator('[data-testid="user-2"]')).toContainText('Bob');
});

test('handle API error gracefully', async ({ page }) => {
  await page.route('**/api/users', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Internal Server Error' })
    });
  });
  
  await page.goto('/users');
  
  await expect(page.locator('.error-message'))
    .toContainText('Failed to load users');
});

// Cypress with network stubbing
cy.intercept('GET', '/api/products', {
  statusCode: 200,
  body: {
    products: [
      { id: 1, name: 'Product 1', price: 29.99 },
      { id: 2, name: 'Product 2', price: 49.99 }
    ]
  }
}).as('getProducts');

cy.visit('/shop');
cy.wait('@getProducts');
cy.get('[data-testid="product"]').should('have.length', 2);
```

### Scenario 2: File Upload Testing

```typescript
// Playwright file upload
test('upload profile picture', async ({ page }) => {
  await page.goto('/profile/edit');
  
  // Set up file chooser listener
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.click('text=Upload Photo');
  const fileChooser = await fileChooserPromise;
  
  // Upload file
  await fileChooser.setFiles('./fixtures/profile-photo.jpg');
  
  // Verify preview
  const preview = page.locator('[data-testid="photo-preview"]');
  await expect(preview).toBeVisible();
  
  // Save changes
  await page.click('button:has-text("Save")');
  
  // Verify upload success
  await expect(page.locator('.success-message')).toContainText('Profile updated');
});

// Cypress file upload
cy.get('input[type="file"]').selectFile('cypress/fixtures/document.pdf');
cy.get('[data-testid="file-name"]').should('contain', 'document.pdf');
cy.get('button:contains("Upload")').click();
cy.get('.upload-status').should('contain', 'Upload complete');
```

### Scenario 3: Multi-Step Form Validation

```typescript
test('wizard form with validation', async ({ page }) => {
  await page.goto('/registration');
  
  // Step 1: Personal Information
  await page.fill('input[name="firstName"]', 'John');
  await page.fill('input[name="lastName"]', 'Doe');
  await page.fill('input[name="email"]', 'john.doe@example.com');
  await page.click('button:has-text("Next")');
  
  // Step 2: Address
  await expect(page.locator('h2')).toContainText('Address Information');
  await page.fill('input[name="street"]', '123 Main St');
  await page.fill('input[name="city"]', 'Boston');
  await page.selectOption('select[name="state"]', 'MA');
  await page.fill('input[name="zipCode"]', '02101');
  await page.click('button:has-text("Next")');
  
  // Step 3: Preferences
  await expect(page.locator('h2')).toContainText('Preferences');
  await page.check('input[name="newsletter"]');
  await page.selectOption('select[name="language"]', 'en');
  
  // Submit
  await page.click('button[type="submit"]');
  
  // Verify success
  await expect(page.locator('.success-message'))
    .toContainText('Registration complete');
});
```

### Scenario 4: Authentication and Authorization

```typescript
test.describe('Protected Routes', () => {
  test('redirect to login when not authenticated', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/.*login/);
  });

  test('admin can access admin panel', async ({ page, context }) => {
    // Set admin auth cookie
    await context.addCookies([{
      name: 'auth_token',
      value: 'admin-token-123',
      domain: 'example.com',
      path: '/'
    }]);
    
    await page.goto('/admin');
    await expect(page.locator('h1')).toContainText('Admin Panel');
  });

  test('regular user cannot access admin panel', async ({ page, context }) => {
    await context.addCookies([{
      name: 'auth_token',
      value: 'user-token-456',
      domain: 'example.com',
      path: '/'
    }]);
    
    await page.goto('/admin');
    await expect(page.locator('.error-message'))
      .toContainText('Access denied');
  });
});
```

## Best Practices

### Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('input[name="email"]', email);
    await this.page.fill('input[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }

  async getErrorMessage() {
    return await this.page.locator('.error-message').textContent();
  }

  async isLoggedIn() {
    await this.page.waitForURL(/.*dashboard/);
    return this.page.url().includes('dashboard');
  }
}

// pages/DashboardPage.ts
export class DashboardPage {
  constructor(private page: Page) {}

  async getUserName() {
    return await this.page.locator('[data-testid="user-name"]').textContent();
  }

  async navigateToSettings() {
    await this.page.click('[data-testid="settings-link"]');
  }

  async logout() {
    await this.page.click('[data-testid="user-menu"]');
    await this.page.click('text=Logout');
  }
}

// Using Page Objects
test('login and navigate', async ({ page }) => {
  const loginPage = new LoginPage(page);
  const dashboardPage = new DashboardPage(page);
  
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');
  
  expect(await loginPage.isLoggedIn()).toBeTruthy();
  expect(await dashboardPage.getUserName()).toBe('John Doe');
  
  await dashboardPage.navigateToSettings();
});
```

### Test Data Management

```typescript
// fixtures/users.json
{
  "admin": {
    "email": "admin@example.com",
    "password": "Admin123!",
    "role": "admin"
  },
  "customer": {
    "email": "customer@example.com",
    "password": "Customer123!",
    "role": "customer"
  }
}

// tests/helpers.ts
import users from '../fixtures/users.json';

export function getUser(role: 'admin' | 'customer') {
  return users[role];
}

export async function loginAs(page: Page, role: 'admin' | 'customer') {
  const user = getUser(role);
  await page.goto('/login');
  await page.fill('input[name="email"]', user.email);
  await page.fill('input[name="password"]', user.password);
  await page.click('button[type="submit"]');
  await page.waitForURL(/.*dashboard/);
}

// Usage in tests
test('admin workflow', async ({ page }) => {
  await loginAs(page, 'admin');
  // Test admin features
});
```

### Waiting Strategies

```typescript
// Wait for element
await page.waitForSelector('[data-testid="results"]');

// Wait for navigation
await page.waitForURL('**/dashboard');

// Wait for network idle
await page.waitForLoadState('networkidle');

// Wait for custom condition
await page.waitForFunction(() => {
  return document.querySelectorAll('.item').length > 5;
});

// Wait for API response
const responsePromise = page.waitForResponse(
  response => response.url().includes('/api/data') && response.status() === 200
);
await page.click('button:has-text("Load Data")');
const response = await responsePromise;
const data = await response.json();
```

### Visual Regression Testing

```typescript
// Playwright screenshot comparison
test('homepage visual test', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
    maxDiffPixels: 100
  });
});

test('button states', async ({ page }) => {
  await page.goto('/components');
  
  const button = page.locator('button.primary');
  
  // Default state
  await expect(button).toHaveScreenshot('button-default.png');
  
  // Hover state
  await button.hover();
  await expect(button).toHaveScreenshot('button-hover.png');
  
  // Disabled state
  await page.evaluate(() => {
    document.querySelector('button.primary').disabled = true;
  });
  await expect(button).toHaveScreenshot('button-disabled.png');
});
```

## Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['json', { outputFile: 'test-results/results.json' }]
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Cypress Configuration

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    experimentalStudio: true,
    setupNodeEvents(on, config) {
      // Email checking task
      on('task', {
        async checkEmail({ to, subject }) {
          // Implementation to check test email
          return { found: true };
        }
      });
      
      // Database seeding
      on('task', {
        async seedDatabase(data) {
          // Seed test database
          return null;
        }
      });
    },
  },
  env: {
    apiUrl: 'http://localhost:4000/api',
  },
  retries: {
    runMode: 2,
    openMode: 0,
  },
});
```

## CI/CD Integration

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright browsers
        run: npx playwright install --with-deps ${{ matrix.browser }}
      
      - name: Run E2E tests
        run: npx playwright test --project=${{ matrix.browser }}
        env:
          CI: true
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results-${{ matrix.browser }}
          path: test-results/
          retention-days: 30
      
      - name: Upload Playwright report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report-${{ matrix.browser }}
          path: playwright-report/
          retention-days: 30
```

## Troubleshooting

### Flaky Tests

```typescript
// Use auto-waiting
await page.click('button'); // Automatically waits for button to be actionable

// Increase timeout for slow operations
await page.waitForSelector('.results', { timeout: 30000 });

// Disable animations
await page.addStyleTag({
  content: '*, *::before, *::after { animation-duration: 0s !important; }'
});

// Wait for network to be idle
await page.waitForLoadState('networkidle');

// Use test.slow() for tests that need more time
test.slow();
test('slow operation', async ({ page }) => {
  // This test gets 3x timeout
});
```

### Debugging

```typescript
// Playwright debugging
test('debug test', async ({ page }) => {
  await page.pause(); // Opens Playwright Inspector
  
  // Step-by-step debugging
  await page.goto('/');
  console.log(await page.title());
  await page.screenshot({ path: 'debug.png' });
});

// Run in headed mode
npx playwright test --headed

// Run in debug mode
npx playwright test --debug

// Cypress debugging
cy.pause(); // Pause execution
cy.debug(); // Enable debugger
cy.log('Custom message');
```

## Related Skills

- **visual-regression-tester**: Compare UI screenshots
- **accessibility-tester**: Test WCAG compliance
- **cross-browser-tester**: Multi-browser testing
- **api-fuzz-tester**: Test API security
- **load-generator**: Performance testing
- **integration-test-builder**: API and backend testing

## References

- [Playwright Documentation](https://playwright.dev/)
- [Cypress Documentation](https://www.cypress.io/)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Page Object Model](https://playwright.dev/docs/pom)
- [Visual Testing](https://playwright.dev/docs/test-snapshots)
