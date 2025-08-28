<script lang="ts">
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/auth';
  import StatsCard from '$lib/components/StatsCard.svelte';
  import RecentApplications from '$lib/components/RecentApplications.svelte';
  import UpcomingInterviews from '$lib/components/UpcomingInterviews.svelte';
  import ActivityFeed from '$lib/components/ActivityFeed.svelte';
  import QuickActions from '$lib/components/QuickActions.svelte';
  import ApplicationChart from '$lib/components/ApplicationChart.svelte';
  
  import type { 
    DashboardStats, 
    Application, 
    Interview, 
    Activity 
  } from '$lib/types/dashboard';
  
  let stats: DashboardStats = {
    totalResumes: 0,
    totalApplications: 0,
    upcomingInterviews: 0,
    responseRate: 0
  };
  
  let recentApplications: Application[] = [];
  let upcomingInterviews: Interview[] = [];
  let activities: Activity[] = [];
  let loading = true;
  let error: string | null = null;
  
  onMount(async () => {
    // Load dashboard data - authentication is handled by layout
    await loadDashboardData();
  });
  
  async function loadDashboardData(): Promise<void> {
    try {
      loading = true;
      error = null;
      
      // Simulate API calls with mock data for now
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      stats = {
        totalResumes: 5,
        totalApplications: 23,
        upcomingInterviews: 3,
        responseRate: 34.8
      };
      
      recentApplications = [
        {
          id: '1',
          company_name: 'TechCorp Inc.',
          job_title: 'Senior Frontend Developer',
          status: 'interview',
          applied_date: '2024-01-15',
          salary_range: '$90k - $120k',
          location: 'San Francisco, CA'
        },
        {
          id: '2',
          company_name: 'StartupXYZ',
          job_title: 'Full Stack Engineer',
          status: 'applied',
          applied_date: '2024-01-14',
          salary_range: '$80k - $110k',
          location: 'Remote'
        },
        {
          id: '3',
          company_name: 'BigTech Solutions',
          job_title: 'React Developer',
          status: 'rejected',
          applied_date: '2024-01-12',
          salary_range: '$85k - $115k',
          location: 'New York, NY'
        }
      ];
      
      upcomingInterviews = [
        {
          id: '1',
          company_name: 'TechCorp Inc.',
          job_title: 'Senior Frontend Developer',
          interview_date: '2024-01-20T14:00:00Z',
          interview_type: 'video',
          status: 'scheduled'
        },
        {
          id: '2',
          company_name: 'Innovation Labs',
          job_title: 'UI/UX Developer',
          interview_date: '2024-01-22T10:30:00Z',
          interview_type: 'phone',
          status: 'scheduled'
        },
        {
          id: '3',
          company_name: 'Digital Solutions',
          job_title: 'Frontend Engineer',
          interview_date: '2024-01-25T16:00:00Z',
          interview_type: 'onsite',
          status: 'pending'
        }
      ];
      
      activities = [
        {
          id: '1',
          type: 'application',
          message: 'Applied to Senior Frontend Developer at TechCorp Inc.',
          timestamp: '2024-01-15T10:30:00Z',
          status: 'success'
        },
        {
          id: '2',
          type: 'interview',
          message: 'Interview scheduled with Innovation Labs',
          timestamp: '2024-01-14T15:45:00Z',
          status: 'info'
        },
        {
          id: '3',
          type: 'response',
          message: 'Received response from BigTech Solutions',
          timestamp: '2024-01-13T09:20:00Z',
          status: 'warning'
        }
      ];
      
    } catch (err) {
      error = 'Failed to load dashboard data';
      console.error('Dashboard data error:', err);
    } finally {
      loading = false;
    }
  }
</script>

<!-- Dashboard Content -->
<div class="space-y-6">
  <!-- Header -->
  <div class="flex justify-between items-center">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
      <p class="text-gray-600">Welcome back, {$user?.first_name}!</p>
    </div>
    <QuickActions />
  </div>

  <!-- Stats Cards -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <StatsCard 
      title="Total Resumes" 
      value={stats.totalResumes} 
      icon="document" 
      trend="+2 this week"
    />
    <StatsCard 
      title="Applications" 
      value={stats.totalApplications} 
      icon="briefcase" 
      trend="+5 this month"
    />
    <StatsCard 
      title="Upcoming Interviews" 
      value={stats.upcomingInterviews} 
      icon="calendar" 
      trend="Next: Tomorrow"
    />
    <StatsCard 
      title="Response Rate" 
      value={`${stats.responseRate}%`} 
      icon="chart" 
      trend="+2.5% this month"
    />
  </div>

  <!-- Charts and Recent Activity -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Application Chart -->
    <div class="lg:col-span-2">
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Application Trends</h3>
        <ApplicationChart />
      </div>
    </div>

    <!-- Activity Feed -->
    <div class="bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
      <ActivityFeed {activities} />
    </div>
  </div>

  <!-- Recent Applications and Interviews -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- Recent Applications -->
    <div class="bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Applications</h3>
      <RecentApplications {recentApplications} />
    </div>

    <!-- Upcoming Interviews -->
    <div class="bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Upcoming Interviews</h3>
      <UpcomingInterviews {upcomingInterviews} />
    </div>
  </div>
</div>

<!-- Loading State -->
{#if loading}
  <div class="flex items-center justify-center h-64">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
  </div>
{/if}

<!-- Error State -->
{#if error}
  <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
    {error}
  </div>
{/if}