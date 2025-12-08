import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState({
    total_alerts: 0,
    active_cameras: 0,
    uptime: 0
  });
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const statsRes = await fetch('http://localhost:8000/stats');
        const statsData = await statsRes.json();
        setStats(statsData);

        const alertsRes = await fetch('http://localhost:8000/alerts');
        const alertsData = await alertsRes.json();
        setAlerts(alertsData);
      } catch (error) {
        console.error("Failed to fetch data:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const formatUptime = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${h}h ${m}m`;
  };

  // Prepare data for charts
  const alertTypes = alerts.reduce((acc, alert) => {
    acc[alert.event] = (acc[alert.event] || 0) + 1;
    return acc;
  }, {});

  const pieData = Object.keys(alertTypes).map(key => ({ name: key, value: alertTypes[key] }));
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#FF0000'];

  return (
    <div className="flex h-screen bg-gray-100 font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col">
        <div className="p-6 border-b border-slate-800">
          <h1 className="text-2xl font-bold tracking-wider text-blue-400">CCTV AI</h1>
          <p className="text-xs text-slate-400 mt-1">Surveillance System</p>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`w-full flex items-center p-3 rounded-lg transition-colors ${activeTab === 'dashboard' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
          >
            <span className="mr-3">📊</span> Dashboard
          </button>
          <button
            onClick={() => setActiveTab('live')}
            className={`w-full flex items-center p-3 rounded-lg transition-colors ${activeTab === 'live' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
          >
            <span className="mr-3">🎥</span> Live Feed
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`w-full flex items-center p-3 rounded-lg transition-colors ${activeTab === 'analytics' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
          >
            <span className="mr-3">📈</span> Analytics
          </button>
          <button
            onClick={() => setActiveTab('alerts')}
            className={`w-full flex items-center p-3 rounded-lg transition-colors ${activeTab === 'alerts' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
          >
            <span className="mr-3">⚠️</span> Alerts
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`w-full flex items-center p-3 rounded-lg transition-colors ${activeTab === 'settings' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
          >
            <span className="mr-3">⚙️</span> Settings
          </button>
        </nav>
        <div className="p-4 border-t border-slate-800">
          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-xs font-bold">ON</div>
            <div className="ml-3">
              <p className="text-sm font-medium">System Status</p>
              <p className="text-xs text-green-400">Active</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        {/* Header */}
        <header className="bg-white shadow-sm p-6 flex justify-between items-center">
          <h2 className="text-2xl font-semibold text-gray-800 capitalize">{activeTab}</h2>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-500">Last updated: Just now</span>
            <button className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors">
              Emergency Stop
            </button>
          </div>
        </header>

        {/* Content Area */}
        <div className="p-6">
          {activeTab === 'dashboard' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {/* Stats Cards */}
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <p className="text-sm text-gray-500 mb-1">Total Alerts</p>
                <h3 className="text-3xl font-bold text-gray-800">{stats.total_alerts}</h3>
                <p className="text-xs text-red-500 mt-2">Recorded events</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <p className="text-sm text-gray-500 mb-1">Active Cameras</p>
                <h3 className="text-3xl font-bold text-gray-800">{stats.active_cameras}</h3>
                <p className="text-xs text-green-500 mt-2">All systems normal</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <p className="text-sm text-gray-500 mb-1">Storage Used</p>
                <h3 className="text-3xl font-bold text-gray-800">45%</h3>
                <p className="text-xs text-blue-500 mt-2">1.2TB / 2TB</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <p className="text-sm text-gray-500 mb-1">Uptime</p>
                <h3 className="text-3xl font-bold text-gray-800">{formatUptime(stats.uptime)}</h3>
                <p className="text-xs text-gray-400 mt-2">Since last reboot</p>
              </div>
            </div>
          )}

          {(activeTab === 'live' || activeTab === 'dashboard') && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <div className="bg-black rounded-xl overflow-hidden aspect-video relative group shadow-lg">
                <div className="absolute top-4 left-4 bg-red-600 text-white text-xs px-2 py-1 rounded animate-pulse z-10">LIVE</div>
                <div className="absolute bottom-4 left-4 text-white text-sm bg-black/50 px-2 py-1 rounded z-10">Camera 01 - Main Feed</div>
                <img
                  src="http://localhost:8000/video_feed"
                  alt="Live Feed"
                  className="w-full h-full object-cover"
                  onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex' }}
                />
                <div className="hidden w-full h-full items-center justify-center text-gray-500 bg-gray-900 absolute top-0 left-0">
                  Connecting to feed...
                </div>
              </div>
              {/* Placeholder for second camera */}
              <div className="bg-black rounded-xl overflow-hidden aspect-video relative group shadow-lg">
                <div className="absolute top-4 left-4 bg-red-600 text-white text-xs px-2 py-1 rounded animate-pulse">LIVE</div>
                <div className="absolute bottom-4 left-4 text-white text-sm bg-black/50 px-2 py-1 rounded">Camera 02 - Parking Lot</div>
                <div className="w-full h-full flex items-center justify-center text-gray-600 bg-gray-900">
                  [Signal Lost]
                </div>
              </div>
            </div>
          )}

          {activeTab === 'analytics' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="text-lg font-semibold mb-4">Alert Distribution</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={pieData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        fill="#8884d8"
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {pieData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
                <div className="h-64 flex items-center justify-center text-gray-400">
                  [Bar Chart Placeholder - Needs more historical data]
                </div>
              </div>
            </div>
          )}

          {(activeTab === 'alerts' || activeTab === 'dashboard') && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <div className="p-6 border-b border-gray-100">
                <h3 className="text-lg font-semibold text-gray-800">Recent Alerts</h3>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
                    <tr>
                      <th className="px-6 py-3">Time</th>
                      <th className="px-6 py-3">Camera</th>
                      <th className="px-6 py-3">Event</th>
                      <th className="px-6 py-3">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {alerts.map((alert, index) => (
                      <tr key={index} className="hover:bg-gray-50">
                        <td className="px-6 py-4 text-sm text-gray-600">{new Date(alert.timestamp).toLocaleTimeString()}</td>
                        <td className="px-6 py-4 text-sm text-gray-800 font-medium">{alert.camera}</td>
                        <td className="px-6 py-4 text-sm">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${alert.event.includes('Critical') || alert.event.includes('fire') || alert.event.includes('knife')
                              ? 'bg-red-100 text-red-600'
                              : 'bg-yellow-100 text-yellow-600'
                            }`}>
                            {alert.event}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">{alert.status}</td>
                      </tr>
                    ))}
                    {alerts.length === 0 && (
                      <tr>
                        <td colSpan="4" className="px-6 py-4 text-center text-gray-500">No alerts recorded yet.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
