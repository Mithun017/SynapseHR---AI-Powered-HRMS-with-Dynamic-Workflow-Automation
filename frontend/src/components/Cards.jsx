import React from 'react';
import { motion } from 'framer-motion';
import { Calendar, DollarSign, UserCheck, AlertCircle, FileText, MoreHorizontal, CheckCircle2 } from 'lucide-react';

const CardWrapper = ({ title, status, children }) => (
  <div className="card-premium">
    <div className="card-header">
      <span className="card-title">{title}</span>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        {status && (
            <span className={`status-badge status-${status.toLowerCase()}`}>
                {status}
            </span>
        )}
        <MoreHorizontal size={18} style={{ color: 'var(--text-muted)', cursor: 'pointer' }} />
      </div>
    </div>
    {children}
  </div>
);

export const LeaveCard = ({ title, data, onAction }) => (
  <CardWrapper title={title} status={data.status || 'Pending'}>
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '1rem' }}>
        <div style={{ background: '#fff7ed', padding: '0.75rem', borderRadius: '10px' }}>
            <Calendar size={24} color="#f97316" />
        </div>
        <div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Request Dates</div>
            <div style={{ fontWeight: '600' }}>{data.date}</div>
        </div>
    </div>
    <div style={{ fontSize: '0.9rem', color: 'var(--text-main)', marginBottom: '1.25rem' }}>
        Type: <span style={{ fontWeight: '500' }}>{data.type || 'Vacation'}</span> <br/>
        Reason: <span style={{ fontWeight: '500' }}>{data.reason}</span>
    </div>
    <div style={{ display: 'flex', gap: '0.5rem' }}>
        <motion.button 
            whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
            className="btn-outline" style={{ flex: 1, fontSize: '0.85rem' }} 
            onClick={() => onAction('ACTION:leave.request')}
        >
            Cancel
        </motion.button>
        <motion.button 
            whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
            className="btn-primary" style={{ flex: 1, fontSize: '0.85rem' }} 
            onClick={() => onAction('ACTION:leave.request')}
        >
            View Details
        </motion.button>
    </div>
  </CardWrapper>
);

export const PayrollCard = ({ title, data, onAction }) => (
  <CardWrapper title={title} status="Approved">
    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
        <div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Net Salary</div>
            <div style={{ fontSize: '1.25rem', fontWeight: '700' }}>{data.salary || '$0.00'}</div>
        </div>
        <div style={{ background: '#f0fdf4', padding: '0.75rem', borderRadius: '10px' }}>
            <DollarSign size={24} color="#10b981" />
        </div>
    </div>
    <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1rem', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.5rem' }}>
            <span color="var(--text-muted)">Tax Deductions</span>
            <span style={{ fontWeight: '600' }}>{data.tax || '$0.00'}</span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
            <span color="var(--text-muted)">Bonuses</span>
            <span style={{ fontWeight: '600', color: 'var(--success)' }}>{data.bonus || '$0.00'}</span>
        </div>
    </div>
    <motion.button 
        whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
        className="btn-primary" style={{ width: '100%' }} 
        onClick={() => onAction('ACTION:payroll.query')}
    >
        View Payslip
    </motion.button>
  </CardWrapper>
);

export const OnboardingCard = ({ title, data, onAction }) => (
  <CardWrapper title={title} status="Active">
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1.5rem' }}>
        { (data.tasks || ["Profile Setup", "Document Signing", "Orientation"]).map((task, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.9rem' }}>
                <div style={{ color: i === 0 ? 'var(--success)' : 'var(--border)' }}>
                    <CheckCircle2 size={18} />
                </div>
                <span style={{ color: i === 0 ? 'var(--text-main)' : 'var(--text-muted)' }}>{task}</span>
            </div>
        ))}
    </div>
    <motion.button 
        whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
        className="btn-primary" style={{ width: '100%' }} 
        onClick={() => onAction('ACTION:onboarding.initiate')}
    >
        Continue Process
    </motion.button>
  </CardWrapper>
);

export const ErrorCard = ({ title, data }) => (
  <div className="card-premium" style={{ borderLeft: '4px solid var(--danger)' }}>
    <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '0.75rem' }}>
        <AlertCircle color="var(--danger)" />
        <span style={{ fontWeight: '700', color: 'var(--danger)' }}>{title}</span>
    </div>
    <p style={{ fontSize: '0.9rem', color: 'var(--text-main)' }}>
        {data?.message || "An unexpected error occurred. Please try again."}
    </p>
  </div>
);

export const FormCard = ({ title, data, onAction }) => (
  <CardWrapper title={title}>
    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>{data.message}</p>
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {data.fields && data.fields.map((f, i) => (
            <div key={i} style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                <label style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase' }}>{f}</label>
                <input type="text" className="chat-input" placeholder={`Enter ${f}...`} style={{ width: '100%' }} />
            </div>
        ))}
        <motion.button 
            whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
            className="btn-primary" style={{ marginTop: '0.5rem' }} 
            onClick={() => onAction('ACTION:leave.request')}
        >
            Submit Details
        </motion.button>
    </div>
  </CardWrapper>
);

export const TableCard = ({ title, data, onAction }) => (
    <CardWrapper title={title}>
        <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
                <thead>
                    <tr style={{ borderBottom: '2px solid var(--border)', textAlign: 'left' }}>
                        {data.columns.map((col, i) => (
                            <th key={i} style={{ padding: '0.75rem 0.5rem', color: 'var(--text-muted)', fontWeight: '600' }}>{col}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.rows.map((row, i) => (
                        <tr key={i} style={{ borderBottom: '1px solid var(--border)' }}>
                            {data.columns.map((col, j) => (
                                <td key={j} style={{ padding: '1rem 0.5rem' }}>{row[col]}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
        <motion.button 
            whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            className="btn-outline" style={{ width: '100%', marginTop: '1rem' }} 
            onClick={() => onAction('ACTION:employee.list')}
        >
            Refresh List
        </motion.button>
    </CardWrapper>
);

export const TicketCard = ({ title, data, onAction }) => {
    const isManager = onAction && data.can_approve; // Authoritative Backend Guard
    const statusColor = {
        "Approved": "#10b981",
        "Denied": "#ef4444",
        "Pending": "#f97316"
    }[data.status] || "#64748b";

    return (
        <CardWrapper title={title} status={data.status}>
            <div style={{ marginBottom: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.75rem' }}>
                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                        <span className="badge" style={{ background: `${statusColor}20`, color: statusColor, fontSize: '0.75rem', fontWeight: '700', padding: '0.25rem 0.6rem', borderRadius: '6px' }}>
                            {data.category || 'General'}
                        </span>
                        {data.employee_name && (
                            <span style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-main)', opacity: 0.8 }}>
                                By {data.employee_name}
                            </span>
                        )}
                    </div>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Ticket #{data.id || 'Pending'}</span>
                </div>
                <h4 style={{ fontSize: '1rem', fontWeight: '700', marginBottom: '0.5rem', color: 'var(--text-main)' }}>{data.title}</h4>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>{data.description}</p>
                {data.manager_notes && (
                    <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#f8fafc', borderRadius: '8px', borderLeft: `3px solid ${statusColor}`, fontSize: '0.85rem' }}>
                        <strong>Note:</strong> {data.manager_notes}
                    </div>
                )}
            </div>
            
            {isManager && data.status === "Pending" && (
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
                    <motion.button 
                        whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                        className="btn-outline" 
                        style={{ flex: 1, fontSize: '0.75rem', padding: '0.5rem', borderColor: '#ef4444', color: '#ef4444' }}
                        onClick={() => onAction(`ACTION:ticket.manage action=update ticket_id=${data.id} new_status=Denied`)}
                    >
                        Deny
                    </motion.button>
                    <motion.button 
                        whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                        className="btn-outline" 
                        style={{ flex: 1, fontSize: '0.75rem', padding: '0.5rem', borderColor: '#f97316', color: '#f97316' }}
                        onClick={() => onAction(`ACTION:ticket.manage action=update ticket_id=${data.id} new_status=Pending notes="Need more info"`)}
                    >
                        Pending
                    </motion.button>
                    <motion.button 
                        whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                        className="btn-primary" 
                        style={{ flex: 1, fontSize: '0.75rem', padding: '0.5rem', background: '#10b981', borderColor: '#10b981' }}
                        onClick={() => onAction(`ACTION:ticket.manage action=update ticket_id=${data.id} new_status=Approved`)}
                    >
                        Approve
                    </motion.button>
                </div>
            )}
        </CardWrapper>
    );
};

import { PieChart, Pie, Cell, ResponsiveContainer, BarChart as ReBarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const COLORS = ['#1e40af', '#3b82f6', '#f97316', '#10b981', '#ef4444'];

export const ChartCard = ({ title, data, onAction }) => {
    const isBar = data.type === 'bar';

    return (
        <CardWrapper title={title}>
            <div style={{ height: '250px', width: '100%', marginBottom: '1rem' }}>
                <ResponsiveContainer width="100%" height="100%">
                    {isBar ? (
                        <ReBarChart data={data.data}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                            <XAxis dataKey="label" fontSize={12} tickLine={false} axisLine={false} />
                            <YAxis fontSize={12} tickLine={false} axisLine={false} />
                            <Tooltip cursor={{fill: '#f8fafc'}} />
                            <Bar dataKey="value" fill="#1e40af" radius={[4, 4, 0, 0]} />
                        </ReBarChart>
                    ) : (
                        <PieChart>
                            <Pie
                                data={data.data}
                                innerRadius={60}
                                outerRadius={80}
                                paddingAngle={5}
                                dataKey="value"
                            >
                                {data.data.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                        </PieChart>
                    )}
                </ResponsiveContainer>
            </div>
            {!isBar && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {data.data.map((item, i) => (
                        <div key={i} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: COLORS[i % COLORS.length] }} />
                                <span>{item.label}</span>
                            </div>
                            <span style={{ fontWeight: '600' }}>{item.value}</span>
                        </div>
                    ))}
                </div>
            )}
            <motion.button 
                whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
                className="btn-primary" style={{ width: '100%', marginTop: '1.25rem' }} 
                onClick={() => onAction('ACTION:analytics.stats')}
            >
                Analyze Trends
            </motion.button>
        </CardWrapper>
    );
};
