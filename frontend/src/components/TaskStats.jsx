const TaskStats = ({ stats = { assigned: 0, completed: 0, posted: 0 } }) => {
  return (
    <div className="task-stats">
      <div className="stat-box">Assigned: {stats.assigned}</div>
      <div className="stat-box">Completed: {stats.completed}</div>
      <div className="stat-box">Posted: {stats.posted}</div>
    </div>
  );
};

export default TaskStats;
