# Retail Product Annotation Guidelines

## Categories

- **Dairy**: milk, butter, cheese, curd, paneer, yogurt, ghee, dairy cream.
- **Snacks**: chips, biscuits, cookies, crackers, chocolate, candy, namkeen, popcorn, protein bars.
- **Beverages**: tea, coffee, juice, soft drinks, water, energy drinks, beverage powders.
- **Personal Care**: soap, shampoo, toothpaste, toothbrushes, skincare, handwash, deodorant, sanitary products.
- **Household**: detergent, dishwashing products, cleaners, disinfectants, tissue, garbage bags, laundry products.
- **Staples**: rice, flour, atta, wheat, salt, sugar, cooking oil, pulses, lentils, spices.
- **Other**: products that do not fit any category above or cannot be categorized from the available name.

## Edge-case rules

1. Classify by the product's primary use, not by an ingredient. Coconut milk soap is Personal Care; coconut milk beverage is Beverages.
2. Protein bars are Snacks.
3. Tea leaves, tea bags, and tea powder intended for making tea are Beverages.
4. Cooking oil is Staples; hair oil is Personal Care.
5. If the product name is blank, do not infer a category; flag it for manual review.
6. If no rule matches or the name is ambiguous, assign `Other` as a provisional fallback and flag it for manual review.
7. A duplicate name is a data-quality issue, not automatically an annotation error. Review whether it is a duplicate record or a separate package size/variant.
8. Reference/gold labels should be checked manually before using their accuracy as a meaningful quality metric.

## Annotation process

Use the suggested category as a starting point, review flags and edge cases, and record a final reviewed label. This tool is a rule-based assistant; it does not replace human verification.
