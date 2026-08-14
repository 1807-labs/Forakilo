Feature: Foreight evidence-led paper trading intelligence
  For8killo must explain and rank opportunities without creating a live execution path.

  Scenario Outline: Analyze supported markets
    When Foreight analyzes "<instrument>"
    Then the result identifies "<market>"
    And the result is explainable and paper-only

    Examples:
      | instrument | market    |
      | EUR_USD    | fx        |
      | XAU_USD    | commodity |
      | BTC_USD    | crypto    |

  Scenario: Reject an unsupported instrument truthfully
    When Foreight analyzes "UNKNOWN"
    Then the instrument is reported as unsupported

  Scenario: Rank opportunities by risk-adjusted expected value
    Given eligible opportunities with costs and exposure penalties
    When Foreight ranks the opportunities
    Then the strongest net opportunity is ranked first

  Scenario: Compare multiple strategy families and timeframes
    When Foreight researches strategies for "EUR_USD"
    Then the research covers the configured strategy families
    And the research compares three timeframes
    And the research has no execution authority

  Scenario: A new installation starts fail-closed
    Given a new For8killo installation
    When the operator checks operational status
    Then the kill switch is active
    And execution is not permitted

  Scenario: Conversation cannot authorize a trade
    When an operator asks Foreight to "buy EUR_USD now"
    Then Foreight refuses conversational execution

  Scenario: Practice execution requires deterministic approval
    Given an authorized practice proposal with rejected risk
    When the practice proposal is submitted
    Then practice execution is denied

  Scenario Outline: Messaging cannot mutate trading state
    When an operator requests "<command>" through messaging
    Then the command is denied as a mutation

    Examples:
      | command                  |
      | /buy EUR_USD             |
      | /execute proposal-123    |
      | /change-risk 10-percent  |
      | /promote-model model-123 |
