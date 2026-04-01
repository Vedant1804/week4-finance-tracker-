##This is where the user gets value. You can use dictionary comprehension to group expenses by category.

def get_category_totals(expenses):
    totals = {}
    for exp in expenses:
        cat = exp['category']
        totals[cat] = totals.get(cat, 0) + exp['amount']
    return totals

def print_text_bar_chart(totals):
    print("\n--- Visual Breakdown ---")
    if not totals: return
    
    max_val = max(totals.values())
    scale = 20 # Max width of the bar
    
    for cat, amount in totals.items():
        bar_length = int((amount / max_val) * scale)
        print(f"{cat:<12} | {'█' * bar_length} ${amo
