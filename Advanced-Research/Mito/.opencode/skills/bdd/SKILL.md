---
name: bdd
description: Behavior-Driven Development with Gherkin, Cucumber, and executable specifications
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: software-development
---

## What I do
- Write BDD scenarios in Gherkin syntax
- Create executable specifications
- Implement step definitions
- Test behavior over implementation
- Bridge technical and business communication

## When to use me
When practicing BDD, creating living documentation, or improving team communication.

## Gherkin Syntax

### Core Keywords
```gherkin
Feature: Search functionality
  As a user
  I want to search for products
  So that I can find what I'm looking for

  Scenario: Successful search
    Given I am on the search page
    When I enter "laptop" in the search box
    And I click the search button
    Then I should see search results
    And the results should contain "laptop"

  Scenario: No results found
    Given I am on the search page
    When I enter "xyz123" in the search box
    And I click the search button
    Then I should see "No results found"
```

### Gherkin Keywords
- **Feature**: High-level description
- **Background**: Preconditions for all scenarios
- **Scenario**: Individual test case
- **Scenario Outline**: Parametrized scenarios with Examples
- **Given**: Preconditions
- **When**: Actions/events
- **Then**: Expected outcomes
- **And/But**: Continue previous step
- **DocString**: Multi-line text
- **DataTable**: Structured data

### Scenario Outline Example
```gherkin
Scenario Outline: Add items to cart
  Given the product "<product>" costs "<price>"
  When I add it to cart
  Then my cart total should be "<total>"

  Examples:
    | product | price | total |
    | Laptop  | 1000  | 1000  |
    | Mouse   | 50    | 1050  |
```

## BDD Best Practices

### Writing Scenarios
- Focus on behavior, not UI
- Use business language
- One assertion per scenario
- Independent scenarios
- Meaningful step definitions

### Step Definitions
- Reusable steps
- Parameterization
- Helper methods
- Assertions

### Tools
- **Cucumber**: Ruby, JS, Java, .NET
- **Behave**: Python
- **SpecFlow**: .NET
- **JBehave**: Java

### Integration
- CI/CD pipeline integration
- Living documentation
- Reporting
- Tags for organization
