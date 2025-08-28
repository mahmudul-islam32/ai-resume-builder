<script lang="ts">
  // Root page - no authentication check needed
  // Layout will handle authentication for protected routes
</script>

<svelte:head>
  <title>AI Resume Builder - Build Your Perfect Resume</title>
  <meta name="description" content="Create professional resumes with AI assistance and track your job applications efficiently." />
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100">
  <!-- Hero Section -->
  <div class="relative overflow-hidden">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-20">
      <div class="text-center">
        <h1 class="text-4xl sm:text-6xl font-extrabold text-gray-900 tracking-tight">
          <span class="block">AI-Powered</span>
          <span class="block text-primary-600">Resume Builder</span>
        </h1>
        <p class="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
          Create professional, ATS-friendly resumes tailored to any job description. 
          Track applications, schedule interviews, and land your dream job faster.
        </p>
        
        <div class="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
          <a href="/register" class="btn btn-primary text-lg px-8 py-3">
            Get Started Free
          </a>
          <a href="/login" class="btn btn-outline text-lg px-8 py-3">
            Sign In
          </a>
        </div>
      </div>
    </div>
  </div>

  <!-- Features Section -->
  <div class="py-16 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center">
        <h2 class="text-3xl font-extrabold text-gray-900">
          Everything you need to land your next job
        </h2>
        <p class="mt-4 text-lg text-gray-600">
          Powerful tools to streamline your job search process
        </p>
      </div>

      <div class="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Feature 1 -->
        <div class="relative p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow">
          <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">AI Resume Builder</h3>
          <p class="text-gray-600">
            Generate professional resumes tailored to specific job descriptions using advanced AI technology.
          </p>
        </div>

        <!-- Feature 2 -->
        <div class="relative p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Application Tracking</h3>
          <p class="text-gray-600">
            Keep track of all your job applications, interview schedules, and application status in one place.
          </p>
        </div>

        <!-- Feature 3 -->
        <div class="relative p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Interview Management</h3>
          <p class="text-gray-600">
            Schedule and manage interviews with built-in calendar integration and preparation tools.
          </p>
        </div>

        <!-- Feature 4 -->
        <div class="relative p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow">
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">ATS Optimization</h3>
          <p class="text-gray-600">
            Ensure your resume passes Applicant Tracking Systems with AI-powered keyword optimization.
          </p>
        </div>

        <!-- Feature 5 -->
        <div class="relative p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow">
          <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Smart Matching</h3>
          <p class="text-gray-600">
            Get personalized job recommendations based on your skills, experience, and preferences.
          </p>
        </div>

        <!-- Feature 6 -->
        <div class="relative p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow">
          <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Analytics & Insights</h3>
          <p class="text-gray-600">
            Track your job search progress with detailed analytics and performance insights.
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- CTA Section -->
  <div class="py-16 bg-primary-600">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h2 class="text-3xl font-extrabold text-white">
        Ready to land your dream job?
      </h2>
      <p class="mt-4 text-xl text-primary-100">
        Join thousands of job seekers who have successfully used our AI-powered platform.
      </p>
      <div class="mt-8">
        <a href="/register" class="btn btn-white text-lg px-8 py-3">
          Start Building Your Resume
        </a>
      </div>
    </div>
  </div>
</div>
