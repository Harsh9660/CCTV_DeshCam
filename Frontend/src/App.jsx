import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, AreaChart, Area } from 'recharts';
import { Moon, Sun, Bell, Filter, Download, Settings, AlertTriangle, Users, Activity, MapPin, Play, Pause, Maximize, ChevronLeft, ChevronRight, Search, Menu, X, Zap } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import { motion, AnimatePresence } from 'framer-motion';

// --- Components ---

const StatCard = ({ title, value, subtext, icon: Icon, color }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="bg-[#0A0A0A] p-6 rounded-2xl shadow-lg border border-white/5 hover:border-violet-500/30 transition-all hover:shadow-[0_0_20px_rgba(139,92,246,0.1)] group relative overflow-hidden"
  >
    <div className="absolute top-0 right-0 w-20 h-20 bg-violet-500/5 rounded-full blur-2xl -mr-10 -mt-10 transition-all group-hover:bg-violet-500/10"></div>
    <div className="flex items-center justify-between relative z-10">
      <div>
        <p className="text-sm font-medium text-gray-400 mb-1 group-hover:text-violet-300 transition-colors">{title}</p>
        <h3 className="text-3xl font-bold text-white tracking-tight">{value}</h3>
        <p className={`text-xs mt-2 font-medium ${color.text}`}>{subtext}</p>
      </div>
      <div className={`p-3 rounded-xl bg-white/5 group-hover:bg-violet-500/20 transition-colors border border-white/5 group-hover:border-violet-500/30`}>
        <Icon className="text-gray-300 group-hover:text-violet-400 transition-colors" size={24} />
      </div>
    </div>
  </motion.div>
);

const LiveFeedCard = ({ camera, status, zone }) => (
  <motion.div
    layout
    className="bg-[#0A0A0A] rounded-2xl overflow-hidden aspect-video relative group shadow-2xl border border-white/10 hover:border-violet-500/50 transition-all"
  >
    <div className={`absolute top-4 left-4 px-3 py-1 rounded-full z-10 flex items-center backdrop-blur-md ${status === 'live' ? 'bg-red-500/80 text-white shadow-[0_0_10px_rgba(239,68,68,0.5)]' : 'bg-gray-800/80 text-gray-400'}`}>
      <span className={`w-2 h-2 rounded-full mr-2 ${status === 'live' ? 'bg-white animate-pulse' : 'bg-gray-500'}`}></span>
      <span className="text-xs font-bold uppercase tracking-wider">{status === 'live' ? 'LIVE' : 'OFFLINE'}</span>
    </div>
    <div className="absolute bottom-4 left-4 right-4 flex justify-between items-end z-10">
      <div className="bg-black/60 backdrop-blur-md px-3 py-2 rounded-lg border border-white/10">
        <p className="text-white text-sm font-medium flex items-center"><MapPin size={14} className="mr-1 text-violet-400" /> {zone}</p>
        <p className="text-gray-400 text-xs">{camera}</p>
      </div>
      <button className="p-2 bg-white/10 hover:bg-violet-600 rounded-lg backdrop-blur-md text-white transition-colors border border-white/10">
        <Maximize size={18} />
      </button>
    </div>
    {status === 'live' ? (
      <img
        src="http://localhost:8000/video_feed"
        alt="Live Feed"
        className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity"
        onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex' }}
      />
    ) : (
      <div className="w-full h-full flex items-center justify-center bg-[#050505]">
        <div className="text-center">
          <Activity className="mx-auto text-gray-800 mb-2" size={32} />
          <p className="text-gray-700 text-sm">Signal Lost</p>
        </div>
      </div>
    )}
    <div className="hidden w-full h-full items-center justify-center text-gray-500 bg-[#050505] absolute top-0 left-0">
      <div className="text-center">
        <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p className="text-xs text-violet-400">Connecting...</p>
      </div>
    </div>
  </motion.div>
);

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [stats, setStats] = useState({ total_alerts: 0, active_cameras: 0, uptime: 0 });
  const [alerts, setAlerts] = useState([]);
  const [filteredAlerts, setFilteredAlerts] = useState([]);

  // Filters
  const [selectedZone, setSelectedZone] = useState('all');
  const [selectedSeverity, setSelectedSeverity] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  // WebSocket
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    ws.onopen = () => toast.success('Connected to System', {
      icon: '💜',
      style: { background: '#0A0A0A', color: '#fff', border: '1px solid #7C3AED' }
    });
    ws.onmessage = (e) => {
      const alert = JSON.parse(e.data);
      setAlerts(prev => [alert, ...prev]);
      if (alert.severity === 'critical') toast.error(alert.event, {
        icon: '🚨',
        style: { background: '#2B1111', color: '#FECACA', border: '1px solid #EF4444' }
      });
    };
    return () => ws.close();
  }, []);

  // Fetch Data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, alertsRes] = await Promise.all([
          fetch('http://localhost:8000/stats'),
          fetch('http://localhost:8000/alerts')
        ]);
        setStats(await statsRes.json());
        setAlerts(await alertsRes.json());
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  // Filtering Logic
  useEffect(() => {
    let result = alerts;
    if (selectedZone !== 'all') result = result.filter(a => a.zone === selectedZone);
    if (selectedSeverity !== 'all') result = result.filter(a => a.severity === selectedSeverity);
    if (searchTerm) result = result.filter(a => a.event.toLowerCase().includes(searchTerm.toLowerCase()));
    setFilteredAlerts(result);
  }, [alerts, selectedZone, selectedSeverity, searchTerm]);

  // Chart Data
  const pieData = Object.entries(filteredAlerts.reduce((acc, curr) => {
    acc[curr.scenario] = (acc[curr.scenario] || 0) + 1;
    return acc;
  }, {})).map(([name, value]) => ({ name: name.replace(/_/g, ' '), value }));

  const COLORS = ['#8B5CF6', '#D946EF', '#F43F5E', '#EC4899', '#A78BFA'];

  return (
    <div className="flex h-screen bg-black font-sans text-gray-100 selection:bg-violet-500/30 selection:text-violet-200 overflow-hidden">
      <Toaster position="top-right" />

      {/* Sidebar */}
      <motion.aside
        initial={{ width: 280 }}
        animate={{ width: sidebarOpen ? 280 : 80 }}
        className="bg-[#050505] border-r border-white/5 flex flex-col z-20 shadow-2xl relative"
      >
        {/* Glow effect behind sidebar */}
        <div className="absolute top-0 left-0 w-full h-full bg-violet-500/5 blur-3xl -z-10 pointer-events-none"></div>

        <div className="p-6 flex items-center justify-between">
          {sidebarOpen ? (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <div className="flex items-center space-x-2">
                <div className="bg-violet-600 p-1.5 rounded-lg shadow-[0_0_15px_rgba(124,58,237,0.5)]">
                  <Zap size={18} className="text-white" fill="currentColor" />
                </div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-violet-400 to-fuchsia-500 bg-clip-text text-transparent">Sparrow</h1>
              </div>
              <p className="text-[10px] text-gray-500 font-medium tracking-[0.2em] uppercase mt-2 ml-1">Safety System</p>
            </motion.div>
          ) : (
            <div className="w-8 h-8 bg-violet-600 rounded-lg mx-auto flex items-center justify-center shadow-[0_0_15px_rgba(124,58,237,0.5)]">
              <Zap size={18} className="text-white" fill="currentColor" />
            </div>
          )}
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-1.5 rounded-lg hover:bg-white/5 text-gray-500 hover:text-white transition-colors">
            {sidebarOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
          </button>
        </div>

        <nav className="flex-1 px-4 space-y-2 mt-4">
          {[
            { id: 'dashboard', icon: Activity, label: 'Dashboard' },
            { id: 'live', icon: Play, label: 'Live Monitor' },
            { id: 'analytics', icon: BarChart, label: 'Analytics' },
            { id: 'alerts', icon: AlertTriangle, label: 'Alerts' },
            { id: 'settings', icon: Settings, label: 'Settings' },
          ].map(item => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center p-3 rounded-xl transition-all duration-300 group relative overflow-hidden ${activeTab === item.id
                  ? 'text-white bg-white/5 shadow-[0_0_20px_rgba(139,92,246,0.1)] border border-white/5'
                  : 'text-gray-500 hover:text-gray-200 hover:bg-white/5 border border-transparent'
                }`}
            >
              {activeTab === item.id && (
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-violet-500 rounded-r-full shadow-[0_0_10px_rgba(139,92,246,0.8)]" />
              )}
              <item.icon size={22} className={`relative z-10 transition-colors ${activeTab === item.id ? 'text-violet-400' : 'text-gray-500 group-hover:text-gray-300'}`} />
              {sidebarOpen && <span className="ml-3 relative z-10 font-medium">{item.label}</span>}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-white/5">
          <div className="bg-[#0A0A0A] rounded-xl p-4 border border-white/5 hover:border-violet-500/20 transition-colors group">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-violet-500 to-fuchsia-500 border border-white/20 shadow-lg group-hover:shadow-violet-500/20 transition-all"></div>
              {sidebarOpen && (
                <div>
                  <p className="text-sm font-medium text-white group-hover:text-violet-200 transition-colors">Admin User</p>
                  <p className="text-xs text-green-400 flex items-center"><span className="w-1.5 h-1.5 bg-green-400 rounded-full mr-1.5 animate-pulse shadow-[0_0_5px_rgba(74,222,128,0.5)]"></span> Online</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative bg-black">
        {/* Ambient Background Glows */}
        <div className="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
          <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-violet-900/10 rounded-full blur-[120px]"></div>
          <div className="absolute bottom-[-10%] left-[10%] w-[400px] h-[400px] bg-fuchsia-900/10 rounded-full blur-[100px]"></div>
        </div>

        {/* Top Bar */}
        <header className="sticky top-0 bg-black/80 backdrop-blur-xl border-b border-white/5 px-8 py-4 flex justify-between items-center z-10">
          <div>
            <h2 className="text-2xl font-bold text-white capitalize tracking-tight">{activeTab}</h2>
            <p className="text-sm text-gray-500 mt-0.5">System Status: <span className="text-green-400 font-medium">Optimal</span></p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="relative hidden md:block group">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-violet-400 transition-colors" size={18} />
              <input
                type="text"
                placeholder="Search..."
                className="pl-10 pr-4 py-2 bg-[#0A0A0A] rounded-xl border border-white/5 focus:border-violet-500/50 focus:ring-2 focus:ring-violet-500/20 text-white w-64 transition-all outline-none placeholder-gray-600"
              />
            </div>
            <button className="p-2 rounded-full bg-[#0A0A0A] text-gray-400 hover:text-white hover:bg-white/10 border border-white/5 transition-all relative hover:border-violet-500/30">
              <Bell size={20} />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-fuchsia-500 rounded-full shadow-[0_0_10px_rgba(217,70,239,0.8)] animate-pulse"></span>
            </button>
          </div>
        </header>

        <div className="p-8 max-w-7xl mx-auto relative z-10">
          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-8"
              >
                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <StatCard
                    title="Total Alerts"
                    value={stats.total_alerts}
                    subtext="+12% from yesterday"
                    icon={AlertTriangle}
                    color={{ text: 'text-fuchsia-400' }}
                  />
                  <StatCard
                    title="Active Cameras"
                    value={stats.active_cameras}
                    subtext="All systems operational"
                    icon={Activity}
                    color={{ text: 'text-green-400' }}
                  />
                  <StatCard
                    title="Staff Present"
                    value="8"
                    subtext="Ratio 1:5 (Optimal)"
                    icon={Users}
                    color={{ text: 'text-violet-400' }}
                  />
                  <StatCard
                    title="System Uptime"
                    value="24h 12m"
                    subtext="Since last maintenance"
                    icon={Settings}
                    color={{ text: 'text-blue-400' }}
                  />
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Live Feed Preview */}
                  <div className="lg:col-span-2 space-y-6">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-bold text-white flex items-center">
                        <span className="w-1 h-6 bg-violet-500 rounded-full mr-3 shadow-[0_0_10px_rgba(139,92,246,0.8)]"></span>
                        Live Monitoring
                      </h3>
                      <button onClick={() => setActiveTab('live')} className="text-sm text-violet-400 hover:text-violet-300 font-medium transition-colors hover:underline decoration-violet-500/30 underline-offset-4">View All</button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <LiveFeedCard camera="Cam 01" status="live" zone="Outdoor Play" />
                      <LiveFeedCard camera="Cam 02" status="offline" zone="Classroom A" />
                    </div>
                  </div>

                  {/* Recent Alerts List */}
                  <div className="bg-[#0A0A0A] rounded-2xl p-6 shadow-lg border border-white/5 relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-fuchsia-500/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
                    <h3 className="text-lg font-bold text-white mb-4 flex items-center relative z-10">
                      <span className="w-1 h-6 bg-fuchsia-500 rounded-full mr-3 shadow-[0_0_10px_rgba(217,70,239,0.8)]"></span>
                      Recent Alerts
                    </h3>
                    <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar relative z-10">
                      {filteredAlerts.slice(0, 5).map((alert, idx) => (
                        <div key={idx} className="flex items-start p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-colors cursor-pointer group border border-transparent hover:border-white/10">
                          <div className={`p-2 rounded-lg mr-3 ${alert.severity === 'critical' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'}`}>
                            <AlertTriangle size={16} />
                          </div>
                          <div className="flex-1">
                            <p className="text-sm font-semibold text-gray-200 group-hover:text-white transition-colors">{alert.event}</p>
                            <p className="text-xs text-gray-500 mt-0.5 group-hover:text-gray-400">{alert.zone} • {new Date(alert.timestamp).toLocaleTimeString()}</p>
                          </div>
                        </div>
                      ))}
                      {filteredAlerts.length === 0 && <p className="text-center text-gray-600 py-4">No recent alerts</p>}
                    </div>
                  </div>
                </div>

                {/* Charts Section */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div className="bg-[#0A0A0A] p-6 rounded-2xl shadow-lg border border-white/5">
                    <h3 className="text-lg font-bold text-white mb-6">Alert Distribution</h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={pieData}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={80}
                            paddingAngle={5}
                            dataKey="value"
                            stroke="none"
                          >
                            {pieData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                          </Pie>
                          <Tooltip contentStyle={{ backgroundColor: '#0A0A0A', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', boxShadow: '0 4px 20px rgba(0,0,0,0.5)' }} />
                          <Legend />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="bg-[#0A0A0A] p-6 rounded-2xl shadow-lg border border-white/5">
                    <h3 className="text-lg font-bold text-white mb-6">Activity Trends</h3>
                    <div className="h-64">
                      <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={[{ name: 'Mon', val: 12 }, { name: 'Tue', val: 19 }, { name: 'Wed', val: 15 }, { name: 'Thu', val: 22 }, { name: 'Fri', val: 30 }, { name: 'Sat', val: 10 }, { name: 'Sun', val: 8 }]}>
                          <defs>
                            <linearGradient id="colorVal" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.5} />
                              <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0} />
                            </linearGradient>
                          </defs>
                          <CartesianGrid strokeDasharray="3 3" stroke="#222" vertical={false} />
                          <XAxis dataKey="name" stroke="#666" axisLine={false} tickLine={false} />
                          <YAxis stroke="#666" axisLine={false} tickLine={false} />
                          <Tooltip contentStyle={{ backgroundColor: '#0A0A0A', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', boxShadow: '0 4px 20px rgba(0,0,0,0.5)' }} />
                          <Area type="monotone" dataKey="val" stroke="#8B5CF6" strokeWidth={3} fillOpacity={1} fill="url(#colorVal)" />
                        </AreaChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'live' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="grid grid-cols-1 lg:grid-cols-2 gap-8"
              >
                <LiveFeedCard camera="Cam 01" status="live" zone="Outdoor Play" />
                <LiveFeedCard camera="Cam 02" status="offline" zone="Classroom A" />
                <LiveFeedCard camera="Cam 03" status="offline" zone="Staff Room" />
                <LiveFeedCard camera="Cam 04" status="offline" zone="Hallway" />
              </motion.div>
            )}

            {activeTab === 'alerts' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="bg-[#0A0A0A] rounded-2xl shadow-lg border border-white/5 overflow-hidden"
              >
                <div className="p-6 border-b border-white/5 flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <h3 className="text-xl font-bold text-white">Alert History</h3>
                  <div className="flex items-center space-x-3">
                    <div className="relative">
                      <Filter className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={16} />
                      <select
                        value={selectedSeverity}
                        onChange={(e) => setSelectedSeverity(e.target.value)}
                        className="pl-9 pr-4 py-2 bg-black/50 border border-white/10 rounded-xl text-sm focus:ring-2 focus:ring-violet-500 text-gray-300 outline-none"
                      >
                        <option value="all">All Severities</option>
                        <option value="critical">Critical</option>
                        <option value="high">High</option>
                      </select>
                    </div>
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={16} />
                      <input
                        type="text"
                        placeholder="Search alerts..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-9 pr-4 py-2 bg-black/50 border border-white/10 rounded-xl text-sm focus:ring-2 focus:ring-violet-500 text-gray-300 outline-none"
                      />
                    </div>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-white/5">
                      <tr>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Time</th>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Zone</th>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Event</th>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Severity</th>
                        <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                      {filteredAlerts.map((alert, idx) => (
                        <tr key={idx} className="hover:bg-white/5 transition-colors">
                          <td className="px-6 py-4 text-sm text-gray-400">{new Date(alert.timestamp).toLocaleTimeString()}</td>
                          <td className="px-6 py-4 text-sm font-medium text-white">{alert.zone}</td>
                          <td className="px-6 py-4 text-sm text-gray-300">{alert.event}</td>
                          <td className="px-6 py-4">
                            <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${alert.severity === 'critical' ? 'bg-red-500/20 text-red-400 border border-red-500/20' :
                                alert.severity === 'high' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/20' :
                                  'bg-violet-500/20 text-violet-400 border border-violet-500/20'
                              }`}>
                              {alert.severity}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-500">{alert.status}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

export default App;
