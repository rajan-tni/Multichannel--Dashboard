<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Channel Sales & Marketing Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .dashboard-header {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 16px;
        }
        
        h1 {
            font-size: 32px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        
        .date-filter {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .date-filter select, .date-filter input {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
        }
        
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .kpi-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .kpi-label {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.6);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .kpi-change {
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .positive {
            color: #10b981;
        }
        
        .negative {
            color: #ef4444;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }
        
        .chart-container {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }
        
        .chart-container:hover {
            transform: scale(1.02);
        }
        
        .chart-title {
            font-size: 18px;
            margin-bottom: 20px;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 600;
        }
        
        .table-container {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        th {
            background: rgba(102, 126, 234, 0.2);
            font-weight: 600;
            position: sticky;
            top: 0;
        }
        
        tr:hover {
            background: rgba(255, 255, 255, 0.05);
        }
        
        .tab-container {
            display: flex;
            gap: 8px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .tab {
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .tab:hover {
            background: rgba(102, 126, 234, 0.3);
        }
        
        .tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: transparent;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
            margin-top: 16px;
        }
        
        .metric-item {
            background: rgba(255, 255, 255, 0.03);
            padding: 12px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .metric-label {
            font-size: 11px;
            color: rgba(255, 255, 255, 0.5);
            margin-bottom: 4px;
        }
        
        .metric-value {
            font-size: 18px;
            font-weight: 600;
        }
        
        canvas {
            max-height: 300px;
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        .refresh-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.3s ease;
        }
        
        .refresh-btn:hover {
            transform: scale(1.05);
        }
        
        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .kpi-container {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard-header">
        <div class="header-top">
            <h1>Omnichannel Performance Dashboard</h1>
            <div class="date-filter">
                <select id="timeRange">
                    <option value="today">Today</option>
                    <option value="week">Last 7 Days</option>
                    <option value="month" selected>Last 30 Days</option>
                    <option value="quarter">Last Quarter</option>
                    <option value="year">Year to Date</option>
                </select>
                <input type="date" id="startDate">
                <input type="date" id="endDate">
                <button class="refresh-btn" onclick="refreshData()">↻ Refresh</button>
            </div>
        </div>
        
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">₹24.7M</div>
                <div class="kpi-change positive">↑ 12.5% vs last period</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Ad Spend</div>
                <div class="kpi-value">₹3.2M</div>
                <div class="kpi-change negative">↑ 8.3% vs last period</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">ROAS</div>
                <div class="kpi-value">7.72x</div>
                <div class="kpi-change positive">↑ 3.8% vs last period</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Net Profit</div>
                <div class="kpi-value">₹8.9M</div>
                <div class="kpi-change positive">↑ 15.2% vs last period</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">CAC</div>
                <div class="kpi-value">₹287</div>
                <div class="kpi-change positive">↓ 5.3% vs last period</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">AOV</div>
                <div class="kpi-value">₹2,450</div>
                <div class="kpi-change positive">↑ 7.8% vs last period</div>
            </div>
        </div>
    </div>
    
    <div class="tab-container">
        <div class="tab active" onclick="switchTab('overview', this)">Overview</div>
        <div class="tab" onclick="switchTab('sales', this)">Sales Channels</div>
        <div class="tab" onclick="switchTab('marketing', this)">Marketing</div>
        <div class="tab" onclick="switchTab('pnl', this)">P&L Analysis</div>
        <div class="tab" onclick="switchTab('cohort', this)">Cohort Analysis</div>
    </div>
    
    <div id="overview" class="tab-content">
        <div class="dashboard-grid">
            <div class="chart-container">
                <h3 class="chart-title">Revenue Trend (30 Days)</h3>
                <canvas id="revenueTrend"></canvas>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">Channel Performance</h3>
                <canvas id="channelPie"></canvas>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">Marketing Mix</h3>
                <canvas id="marketingMix"></canvas>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">Conversion Funnel</h3>
                <canvas id="conversionFunnel"></canvas>
            </div>
        </div>
        
        <div class="table-container">
            <h3 class="chart-title">Top Performing Channels - Quick View</h3>
            <table>
                <thead>
                    <tr>
                        <th>Channel</th>
                        <th>Revenue</th>
                        <th>Orders</th>
                        <th>Ad Spend</th>
                        <th>ROAS</th>
                        <th>Profit Margin</th>
                        <th>Trend</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Amazon</td>
                        <td>₹8,250,000</td>
                        <td>3,367</td>
                        <td>₹825,000</td>
                        <td>10.0x</td>
                        <td>28.5%</td>
                        <td class="positive">↑ 12%</td>
                    </tr>
                    <tr>
                        <td>D2C Website</td>
                        <td>₹5,120,000</td>
                        <td>2,089</td>
                        <td>₹640,000</td>
                        <td>8.0x</td>
                        <td>35.2%</td>
                        <td class="positive">↑ 18%</td>
                    </tr>
                    <tr>
                        <td>Flipkart</td>
                        <td>₹4,890,000</td>
                        <td>1,996</td>
                        <td>₹570,000</td>
                        <td>8.6x</td>
                        <td>26.8%</td>
                        <td class="positive">↑ 5%</td>
                    </tr>
                    <tr>
                        <td>Quick Commerce</td>
                        <td>₹3,240,000</td>
                        <td>1,620</td>
                        <td>₹485,000</td>
                        <td>6.7x</td>
                        <td>22.4%</td>
                        <td class="positive">↑ 25%</td>
                    </tr>
                    <tr>
                        <td>Offline</td>
                        <td>₹3,100,000</td>
                        <td>1,240</td>
                        <td>₹680,000</td>
                        <td>4.6x</td>
                        <td>31.5%</td>
                        <td class="negative">↓ 3%</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="dashboard-grid" style="margin-top: 24px;">
            <div class="chart-container">
                <h3 class="chart-title">LTV by Acquisition Channel</h3>
                <canvas id="ltvChannel"></canvas>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">Customer Segment Value</h3>
                <canvas id="segmentValue"></canvas>
            </div>
        </div>
    </div>
    
    <div id="sales" class="tab-content" style="display:none;">
        <div class="dashboard-grid">
            <div class="chart-container full-width">
                <h3 class="chart-title">Sales Channel Performance Comparison</h3>
                <canvas id="salesComparison"></canvas>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">E-commerce Platforms Breakdown</h3>
                <div class="metric-grid">
                    <div class="metric-item">
                        <div class="metric-label">Amazon</div>
                        <div class="metric-value">₹8.25M</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Flipkart</div>
                        <div class="metric-value">₹4.89M</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">TataCliq</div>
                        <div class="metric-value">₹1.23M</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Others</div>
                        <div class="metric-value">₹0.85M</div>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">Quick Commerce Performance</h3>
                <div class="metric-grid">
                    <div class="metric-item">
                        <div class="metric-label">Zepto</div>
                        <div class="metric-value">₹1.12M</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Blinkit</div>
                        <div class="metric-value">₹0.98M</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Instamart</div>
                        <div class="metric-value">₹0.76M</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">BigBasket</div>
                        <div class="metric-value">₹0.38M</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div id="marketing" class="tab-content" style="display:none;">
        <div class="dashboard-grid">
            <div class="chart-container full-width">
                <h3 class="chart-title">Marketing Spend vs Revenue by Platform</h3>
                <canvas id="marketingROI"></canvas>
            </div>
            
            <div class="table-container full-width">
                <h3 class="chart-title">Marketing Platform Performance</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Platform</th>
                            <th>Spend</th>
                            <th>Impressions</th>
                            <th>Clicks</th>
                            <th>CTR</th>
                            <th>Conversions</th>
                            <th>CPA</th>
                            <th>Revenue</th>
                            <th>ROAS</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Google Ads</td>
                            <td>₹850,000</td>
                            <td>12.5M</td>
                            <td>185K</td>
                            <td>1.48%</td>
                            <td>3,250</td>
                            <td>₹262</td>
                            <td>₹6,800,000</td>
                            <td>8.0x</td>
                        </tr>
                        <tr>
                            <td>Meta (FB & IG)</td>
                            <td>₹720,000</td>
                            <td>18.2M</td>
                            <td>145K</td>
                            <td>0.80%</td>
                            <td>2,880</td>
                            <td>₹250</td>
                            <td>₹5,040,000</td>
                            <td>7.0x</td>
                        </tr>
                        <tr>
                            <td>Amazon Ads</td>
                            <td>₹580,000</td>
                            <td>8.7M</td>
                            <td>122K</td>
                            <td>1.40%</td>
                            <td>2,320</td>
                            <td>₹250</td>
                            <td>₹5,220,000</td>
                            <td>9.0x</td>
                        </tr>
                        <tr>
                            <td>YouTube Ads</td>
                            <td>₹320,000</td>
                            <td>25.6M</td>
                            <td>51K</td>
                            <td>0.20%</td>
                            <td>960</td>
                            <td>₹333</td>
                            <td>₹1,920,000</td>
                            <td>6.0x</td>
                        </tr>
                        <tr>
                            <td>Others</td>
                            <td>₹730,000</td>
                            <td>15.3M</td>
                            <td>95K</td>
                            <td>0.62%</td>
                            <td>1,825</td>
                            <td>₹400</td>
                            <td>₹3,650,000</td>
                            <td>5.0x</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <div id="pnl" class="tab-content" style="display:none;">
        <div class="table-container">
            <h3 class="chart-title">P&L Statement - All Channels Combined</h3>
            <table>
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>This Month</th>
                        <th>Last Month</th>
                        <th>Change %</th>
                        <th>YTD</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="font-weight: bold; background: rgba(102, 126, 234, 0.1);">
                        <td>Gross Revenue</td>
                        <td>₹24,700,000</td>
                        <td>₹21,950,000</td>
                        <td class="positive">+12.5%</td>
                        <td>₹186,200,000</td>
                    </tr>
                    <tr>
                        <td>(-) Returns & Refunds</td>
                        <td>₹1,235,000</td>
                        <td>₹1,097,500</td>
                        <td class="negative">+12.5%</td>
                        <td>₹9,310,000</td>
                    </tr>
                    <tr style="font-weight: bold;">
                        <td>Net Revenue</td>
                        <td>₹23,465,000</td>
                        <td>₹20,852,500</td>
                        <td class="positive">+12.5%</td>
                        <td>₹176,890,000</td>
                    </tr>
                    <tr>
                        <td>(-) COGS</td>
                        <td>₹9,386,000</td>
                        <td>₹8,341,000</td>
                        <td class="negative">+12.5%</td>
                        <td>₹70,756,000</td>
                    </tr>
                    <tr style="font-weight: bold; background: rgba(102, 126, 234, 0.1);">
                        <td>Gross Profit</td>
                        <td>₹14,079,000</td>
                        <td>₹12,511,500</td>
                        <td class="positive">+12.5%</td>
                        <td>₹106,134,000</td>
                    </tr>
                    <tr>
                        <td>(-) Marketing Spend</td>
                        <td>₹3,200,000</td>
                        <td>₹2,955,000</td>
                        <td class="negative">+8.3%</td>
                        <td>₹24,120,000</td>
                    </tr>
                    <tr>
                        <td>(-) Platform Fees</td>
                        <td>₹1,482,000</td>
                        <td>₹1,317,000</td>
                        <td class="negative">+12.5%</td>
                        <td>₹11,173,400</td>
                    </tr>
                    <tr>
                        <td>(-) Logistics</td>
                        <td>₹988,000</td>
                        <td>₹878,000</td>
                        <td class="negative">+12.5%</td>
                        <td>₹7,448,800</td>
                    </tr>
                    <tr>
                        <td>(-) Other OpEx</td>
                        <td>₹741,000</td>
                        <td>₹658,500</td>
                        <td class="negative">+12.5%</td>
                        <td>₹5,586,700</td>
                    </tr>
                    <tr style="font-weight: bold; background: rgba(102, 126, 234, 0.1);">
                        <td>EBITDA</td>
                        <td>₹7,668,000</td>
                        <td>₹6,703,000</td>
                        <td class="positive">+14.4%</td>
                        <td>₹57,805,100</td>
                    </tr>
                    <tr>
                        <td>(-) Depreciation</td>
                        <td>₹247,000</td>
                        <td>₹247,000</td>
                        <td>0%</td>
                        <td>₹1,862,000</td>
                    </tr>
                    <tr>
                        <td>(-) Interest</td>
                        <td>₹123,500</td>
                        <td>₹123,500</td>
                        <td>0%</td>
                        <td>₹931,000</td>
                    </tr>
                    <tr style="font-weight: bold; background: rgba(102, 126, 234, 0.2);">
                        <td>Net Profit</td>
                        <td>₹7,297,500</td>
                        <td>₹6,332,500</td>
                        <td class="positive">+15.2%</td>
                        <td>₹55,012,100</td>
                    </tr>
                    <tr style="font-weight: bold;">
                        <td>Net Margin %</td>
                        <td>29.5%</td>
                        <td>28.8%</td>
                        <td class="positive">+0.7pp</td>
                        <td>29.5%</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="dashboard-grid" style="margin-top: 24px;">
            <div class="chart-container">
                <h3 class="chart-title">Margin Trend</h3>
                <canvas id="marginTrend"></canvas>
            </div>
            
            <div class="chart-container">
                <h3 class="chart-title">Cost Breakdown</h3>
                <canvas id="costBreakdown"></canvas>
            </div>
        </div>
    </div>
    
    <div id="cohort" class="tab-content" style="display:none;">
        <div class="table-container">
            <h3 class="chart-title">Customer Cohort Analysis - Monthly Retention</h3>
            <table>
                <thead>
                    <tr>
                        <th>Cohort</th>
                        <th>Users</th>
                        <th>Month 0</th>
                        <th>Month 1</th>
                        <th>Month 2</th>
                        <th>Month 3</th>
                        <th>Month 4</th>
                        <th>Month 5</th>
                        <th>Month 6</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Jan 2025</td>
                        <td>2,450</td>
                        <td style="background: rgba(102, 126, 234, 0.8);">100%</td>
                        <td style="background: rgba(102, 126, 234, 0.7);">-</td>
                        <td>-</td>
                        <td>-</td>
                        <td>-</td>
                        <td>-</td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td>Dec 2024</td>
                        <td>2,180</td>
                        <td style="background: rgba(102, 126, 234, 0.8);">100%</td>
                        <td style="background: rgba(102, 126, 234, 0.65);">42%</td>
                        <td style="background: rgba(102, 126, 234, 0.55);">35%</td>
                        <td>-</td>
                        <td>-</td>
                        <td>-</td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td>Nov 2024</td>
                        <td>2,340</td>
                        <td style="background: rgba(102, 126, 234, 0.8);">100%</td>
                        <td style="background: rgba(102, 126, 234, 0.68);">45%</td>
                        <td style="background: rgba(102, 126, 234, 0.58);">38%</td>
                        <td style="background: rgba(102, 126, 234, 0.48);">32%</td>
                        <td>-</td>
                        <td>-</td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td>Oct 2024</td>
                        <td>1,980</td>
                        <td style="background: rgba(102, 126, 234, 0.8);">100%</td>
                        <td style="background: rgba(102, 126, 234, 0.66);">44%</td>
                        <td style="background: rgba(102, 126, 234, 0.56);">36%</td>
                        <td style="background: rgba(102, 126, 234, 0.46);">31%</td>
                        <td style="background: rgba(102, 126, 234, 0.42);">28%</td>
                        <td>-</td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td>Sep 2024</td>
                        <td>2,120</td>
                        <td style="background: rgba(102, 126, 234, 0.8);">100%</td>
                        <td style="background: rgba(102, 126, 234, 0.7);">48%</td>
                        <td style="background: rgba(102, 126, 234, 0.6);">40%</td>
                        <td style="background: rgba(102, 126, 234, 0.5);">34%</td>
                        <td style="background: rgba(102, 126, 234, 0.45);">30%</td>
                        <td style="background: rgba(102, 126, 234, 0.4);">27%</td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td>Aug 2024</td>
                        <td>1,850</td>
                        <td style="background: rgba(102, 126, 234, 0.8);">100%</td>
                        <td style="background: rgba(102, 126, 234, 0.65);">43%</td>
                        <td style="background: rgba(102, 126, 234, 0.55);">35%</td>
                        <td style="background: rgba(102, 126, 234, 0.45);">30%</td>
                        <td style="background: rgba(102, 126, 234, 0.4);">26%</td>
                        <td style="background: rgba(102, 126, 234, 0.38);">24%</td>
                        <td style="background: rgba(102, 126, 234, 0.35);">22%</td>
