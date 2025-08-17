<script lang="ts">
  import { onMount } from 'svelte';
  import { user } from '$lib/stores/auth';
  import { goto } from '$app/navigation';
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
    // Check authentication
    if (!$user) {
      goto('/login');
      return;
    }
    
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
        }
      ];
      
      activities = [
        {
          id: '1',
          type: 'application',
          title: 'New Application Submitted',
          description: 'Applied to Frontend Developer at TechCorp Inc.',
          timestamp: '2024-01-15T09:30:00Z'
        },
        {
          id: '2',
          type: 'interview',
          title: 'Interview Scheduled',
          description: 'Video interview with TechCorp Inc. scheduled for Jan 20',
          timestamp: '2024-01-15T14:20:00Z'
        },
        {
          id: '3',
          type: 'resume_update',
          title: 'Resume Updated',
          description: 'Updated resume "Senior Developer Resume" with new skills',
          timestamp: '2024-01-14T16:45:00Z'
        }
      ];
      
    } catch (err) {
      error = 'Failed to load dashboard data';
      console.error('Dashboard error:', err);
    } finally {
      loading = false;
    }
  }
  
  function handleRefresh(): void {
    loadDashboardData();
  }
</script>

<svelte:head>
  <title>Dashboard - AI Resume Builder</title>
</svelte:head>

<div class="px-4 sm:px-6 lg:px-8">
  <!-- Header -->
  <div class="mb-8">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">
          Welcome back, {$user?.first_name || 'User'}!
        </h1>
        <p class="mt-2 text-gray-600">
          Here's what's happening with your job search today.
        </p>
      </div>
      <button
        on:click={handleRefresh}
        disabled={loading}
        class="btn btn-primary flex items-center space-x-2"
      >
        <svg class="w-4 h-4 {loading ? 'animate-spin' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span>{loading ? 'Refreshing...' : 'Refresh'}</span>
      </button>
    </div>
  </div>

  {#if error}
    <div class="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
      <div class="flex">
        <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div class="ml-3">
          <p class="text-sm text-red-800">{error}</p>
        </div>
      </div>
    </div>
  {/if}

  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      <span class="ml-3 text-gray-600">Loading dashboard...</span>
    </div>
  {:else}
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatsCard
        title="Total Resumes"
        value={stats.totalResumes}
        icon="document"
        trend="+2 this month"
        trendDirection="up"
      />
      <StatsCard
        title="Applications Sent"
        value={stats.totalApplications}
        icon="send"
        trend="+5 this week"
        trendDirection="up"
      />
      <StatsCard
        title="Upcoming Interviews"
        value={stats.upcomingInterviews}
        icon="calendar"
        trend="2 this week"
        trendDirection="neutral"
      />
      <StatsCard
        title="Response Rate"
        value="{stats.responseRate}%"
        icon="trending"
        trend="+2.3% from last month"
        trendDirection="up"
      />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
      <!-- Chart -->
      <div class="lg:col-span-2">
        <ApplicationChart />
      </div>
      
      <!-- Quick Actions -->
      <div>
        <QuickActions />
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Recent Applications -->
      <div class="space-y-6">
        <RecentApplications applications={recentApplications} />
        <UpcomingInterviews interviews={upcomingInterviews} />
      </div>
      
      <!-- Activity Feed -->
      <div>
        <ActivityFeed activities={activities} />
      </div>
    </div>
  {/if}
</div>