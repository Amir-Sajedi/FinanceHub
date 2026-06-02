# Net Worth / Credits Feature Documentation

## Overview
This feature allows users to track their personal holdings in gold (18K and 24K) and USD, calculating their total net worth in IRR using real-time market rates.

## Features Implemented

### 1. Database Models (`conversionapp/models.py`)
- **UserHolding**: Stores per-user holdings
  - `gold18`: Gold 18K in grams (Decimal)
  - `gold24`: Gold 24K in grams (Decimal)
  - `usd`: US Dollars (Decimal)
  - One-to-one relationship with User
  - `calculate_net_worth()` method for real-time valuation

- **NetWorthHistory**: Timestamped snapshots for charting
  - `net_worth`: Total value in IRR
  - `gold18_amount`, `gold24_amount`, `usd_amount`: Holdings at snapshot time
  - `timestamp`: When the snapshot was taken
  - Indexed for efficient queries

### 2. Views (`conversionapp/views.py`)
- **NetWorthView**: 
  - GET: Displays current holdings, net worth, and history chart
  - POST: Handles two actions:
    - `update_holdings`: Updates user's holdings
    - `save_snapshot`: Creates a timestamped net worth record

### 3. Templates (`conversionapp/templates/conversionapp/networth.html`)
- Real-time net worth display card matching existing UI design
- Holdings input form with live calculation as user types
- Asset breakdown showing value per asset type
- Chart.js-powered history visualization
- Current market rates reference section
- Navigation link back to converter

### 4. URL Routing (`conversionapp/urls.py`)
- `/hub/networth/` - Net Worth Tracker page

### 5. Admin Interface (`conversionapp/admin.py`)
- UserHolding: Full CRUD access
- NetWorthHistory: Read-only (no manual creation)

## How It Works

### Real-Time Rate Calculation
1. Rates are fetched from `scraper.py` (no hardcoded values)
2. Net worth = (gold18 × gold18_rate) + (gold24 × gold24_rate) + (usd × usd_rate)
3. All calculations happen in IRR (Iranian Rial)

### Data Flow
```
User Input → UserHolding Model → calculate_net_worth() 
                                        ↓
                              Live Rates from Scraper
                                        ↓
                              Net Worth in IRR
                                        ↓
                              Display + Optional Snapshot
```

### History Tracking
- Users click "Save Snapshot" to record their current net worth
- Snapshots include timestamp and holdings amounts
- Chart displays last 30 days of history
- Chart auto-updates when new snapshots are saved

## User Workflow

1. **Access Net Worth Tracker**
   - Navigate from converter page via "View Net Worth Tracker" button
   - Or directly visit `/hub/networth/`

2. **Update Holdings**
   - Enter amounts for gold 18K, gold 24K, and USD
   - Net worth updates in real-time as you type
   - Click "Update Holdings" to save

3. **Track History**
   - Click "Save Snapshot" to record current net worth
   - View historical performance on the chart
   - Chart shows trends over the last 30 days

4. **Review Breakdown**
   - See value contribution from each asset
   - Current market rates displayed at bottom

## Technical Details

### Database Migrations
- `0001_initial.py`: Creates UserHolding and NetWorthHistory tables
- Run `python manage.py migrate conversionapp` to apply

### Dependencies
- Chart.js 4.4.0 (CDN): For history visualization
- Existing scraper module: For live market rates
- Django authentication: Login required for all features

### Security
- LoginRequiredMixin ensures authenticated access only
- CSRF protection on all POST requests
- Decimal fields prevent floating-point errors
- Input validation on form submissions

### Styling
- Matches existing card design with gradient borders
- Uses existing CSS variables from `converter.css`
- Responsive design for mobile/tablet
- Consistent with converter page aesthetics

## API Endpoints

### POST /hub/networth/
```python
# Update holdings
{
    "action": "update_holdings",
    "gold18": "10.500",
    "gold24": "5.250",
    "usd": "1000.00"
}

# Save snapshot
{
    "action": "save_snapshot"
}
```

## Files Modified/Created

### Created
- `conversionapp/models.py` (updated)
- `conversionapp/views.py` (updated)
- `conversionapp/urls.py` (updated)
- `conversionapp/admin.py` (created)
- `conversionapp/migrations/0001_initial.py` (created)
- `conversionapp/templates/conversionapp/networth.html` (created)

### Modified
- `conversionapp/templates/conversionapp/converter.html` (added navigation link)

## Testing Checklist

- [ ] Apply migrations: `python manage.py migrate conversionapp`
- [ ] Create test user and login
- [ ] Access `/hub/networth/` page
- [ ] Enter holdings and verify real-time calculation
- [ ] Update holdings and verify save
- [ ] Save snapshot and verify chart updates
- [ ] Verify asset breakdown calculations
- [ ] Test navigation between converter and net worth pages
- [ ] Check admin interface for both models
- [ ] Verify responsive design on mobile

## Future Enhancements

- Auto-snapshot scheduling (daily/weekly)
- Export history to CSV/PDF
- Comparative analytics (week-over-week, month-over-month)
- Multi-currency support
- Portfolio allocation pie chart
- Price alerts when net worth crosses thresholds
- Integration with cryptocurrency holdings

## Notes

- All rate calculations use live data from tgju.org
- History is retained indefinitely (consider archival policy)
- Chart shows maximum 30 days to maintain performance
- Snapshots are user-initiated (not automatic)
