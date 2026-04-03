import React from 'react';
import { LeaveCard, OnboardingCard, ErrorCard, FormCard, PayslipCard } from './Cards';

const DynamicUI = ({ uiDescriptor }) => {
  if (!uiDescriptor) return null;

  const { ui_type, title, data, actions } = uiDescriptor;

  switch (ui_type) {
    case 'leave_card':
      return <LeaveCard title={title} data={data} />;
    case 'onboarding_card':
      return <OnboardingCard title={title} data={data} />;
    case 'error_card':
      return <ErrorCard title={title} data={data} />;
    case 'form_card':
      return <FormCard title={title} data={data} />;
    case 'payslip_card':
      return <PayslipCard title={title} data={data} />;
    case 'text':
      return <div className="card">{data.text}</div>;
    default:
      return (
        <div className="card">
          <div className="card-title">{title || "Unknown UI Type"}</div>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      );
  }
};

export default DynamicUI;
