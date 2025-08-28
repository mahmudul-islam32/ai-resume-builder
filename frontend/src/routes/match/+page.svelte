<script lang="ts">
  import { writable } from 'svelte/store';
  import { uploadResume, scrapeJobLink } from '$lib/services/dashboard';
  import { computeEnhancedAtsScore } from '$lib/services/enhancedAtsScorer';
  import { auditResume, type AuditReport } from '$lib/services/atsAudit';
  import { scoreResume, type AtsScoreResponse } from '$lib/services/atsApi';
  import JobPostingDisplay from '$lib/components/JobPostingDisplay.svelte';
  import RichTextEditor from '$lib/components/RichTextEditor.svelte';
  import { PDFService } from '$lib/services/pdfService';
  import { onMount } from 'svelte';

  // State
  const jobText = writable<string>('');
  const jobData = writable<any>(null);
  const myResume = writable<{ name: string; text: string; file?: File } | null>(null);
  const myAts = writable<AtsScoreResponse | null>(null);
  const myAudit = writable<AuditReport | null>(null);
  const errorMsg = writable<string | null>(null);
  const useBackend = writable<boolean>(true);

  // UI State
  let jobUrl = '';
  let loadingJob = false;
  let loadingResume = false;
  let showJobEditor = false;
  let showResumeEditor = false;
  let resumePdfUrl = '';
  let jobEditorContent = '';
  let resumeEditorContent = '';



  onMount(() => {
    // Initialize editor content
    jobText.subscribe(content => {
      jobEditorContent = content;
    });
    
    myResume.subscribe(resume => {
      if (resume) {
        resumeEditorContent = resume.text;
      }
    });
  });

  // Actions
  async function handleJobScrape() {
    errorMsg.set(null);
    if (!jobUrl) return;
    loadingJob = true;
    try {
      const job = await scrapeJobLink(jobUrl);
      jobText.set(job?.description ?? '');
      jobEditorContent = job?.description ?? '';
      
      jobData.set({
        title: job?.title || 'Job Title',
        company: job?.company || 'Company',
        description: job?.description || '',
        requirements: job?.requirements || '',
        location: job?.location || '',
        salary_range: job?.salary_range || '',
        url: job?.url || jobUrl
      });
      
      recompute();
    } catch (e) {
      console.error(e);
      errorMsg.set('Failed to scrape the job post.');
    } finally {
      loadingJob = false;
    }
  }

  async function handleResumeChange(e: Event) {
    const input = e.target as HTMLInputElement;
    const f = input.files && input.files[0];
    if (!f) return;
    loadingResume = true;
    try {
      const res = await uploadResume(f);
      myResume.set({ name: f.name, text: res?.parsed_content ?? '', file: f });
      resumeEditorContent = res?.parsed_content ?? '';
      
      // Create PDF URL for display
      if (f.type === 'application/pdf') {
        resumePdfUrl = URL.createObjectURL(f);
      }
      
      await recompute();
    } catch (e) {
      console.error(e);
      errorMsg.set('Failed to parse your resume.');
    } finally {
      loadingResume = false;
      (e.target as HTMLInputElement).value = '';
    }
  }

  function toggleJobEditor() {
    showJobEditor = !showJobEditor;
  }

  function toggleResumeEditor() {
    showResumeEditor = !showResumeEditor;
  }

  function saveJobChanges() {
    jobText.set(jobEditorContent);
    if ($jobData) {
      jobData.set({
        ...$jobData,
        description: jobEditorContent
      });
    }
    showJobEditor = false;
    recompute();
  }

  function saveResumeChanges() {
    if ($myResume) {
      myResume.set({
        ...$myResume,
        text: resumeEditorContent
      });
    }
    showResumeEditor = false;
    recompute();
  }

  async function downloadResumeAsPdf() {
    try {
      const pdfBlob = await PDFService.generateResumePDF(resumeEditorContent, {
        title: 'Professional Resume',
        author: 'AI Resume Builder',
        subject: 'Resume',
        fontSize: 12,
        lineHeight: 1.4,
        margins: { top: 25, bottom: 25, left: 25, right: 25 }
      });
      
      PDFService.downloadPDF(pdfBlob, 'resume.pdf');
    } catch (error) {
      console.error('Error generating PDF:', error);
      errorMsg.set('Failed to generate PDF. Please try again.');
    }
  }

  async function recompute() {
    let jd = '';
    let mine = $myResume;

    jobText.subscribe(v => jd = v)();

    if (!mine) { myAts.set(null); myAudit.set(null); return; }

    myAudit.set(auditResume(mine.text));
    
    if (jd) {
      try {
        if ($useBackend) {
          const requestData = {
            resume_text: mine.text,
            job_description: jd
          };
          
          if (!mine.text || mine.text.trim().length === 0) {
            console.error('ATS Error: Resume text is empty');
            errorMsg.set('Resume text is empty. Please upload a resume first.');
            return;
          }
          
          if (!jd || jd.trim().length === 0) {
            console.error('ATS Error: Job description is empty');
            errorMsg.set('Job description is empty. Please enter a job description.');
            return;
          }
          
          console.log('Sending ATS request:', {
            resume_text_length: mine.text.length,
            job_description_length: jd.length,
            resume_text_preview: mine.text.substring(0, 100) + '...',
            job_description_preview: jd.substring(0, 100) + '...'
          });
          
          const result = await scoreResume(requestData);
          myAts.set(result);
        } else {
          const result = computeEnhancedAtsScore(mine.text, jd);
          myAts.set({
            overall_score: result.overallScore,
            keyword_score: result.keywordScore,
            semantic_score: result.semanticScore,
            format_score: result.formatScore,
            experience_score: result.experienceScore,
            keyword_analysis: {
              required: result.keywordAnalysis.required,
              preferred: result.keywordAnalysis.preferred,
              industry: result.keywordAnalysis.industry,
              soft_skills: result.keywordAnalysis.softSkills
            },
            semantic_analysis: {
              job_title_match: result.semanticAnalysis.jobTitleMatch,
              industry_alignment: result.semanticAnalysis.industryAlignment,
              experience_level: result.semanticAnalysis.experienceLevel,
              responsibility_match: result.semanticAnalysis.responsibilityMatch
            },
            format_analysis: {
              structure_score: result.formatAnalysis.structureScore,
              readability_score: result.formatAnalysis.readabilityScore,
              keyword_density: result.formatAnalysis.keywordDensity,
              section_completeness: result.formatAnalysis.sectionCompleteness
            },
            experience_analysis: {
              years_of_experience: result.experienceAnalysis.yearsOfExperience,
              relevant_experience: result.experienceAnalysis.relevantExperience,
              project_match: result.experienceAnalysis.projectMatch,
              achievement_alignment: result.experienceAnalysis.achievementAlignment
            },
            suggestions: result.suggestions,
            improvements: result.improvements,
            confidence: result.confidence
          });
        }
      } catch (e) {
        console.error('ATS scoring error:', e);
        errorMsg.set('Failed to compute ATS score.');
      }
    } else {
      myAts.set(null);
    }
  }

  // Update job data when job text changes manually
  $: if ($jobText && !$jobData) {
    jobData.set({
      title: 'Job Title',
      company: 'Company',
      description: $jobText,
      requirements: '',
      location: '',
      salary_range: '',
      url: ''
    });
  }
</script>

<header class="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-6 px-8 mb-8">
  <div class="max-w-7xl mx-auto">
    <h1 class="text-3xl font-bold mb-2">Professional ATS Score & Analysis</h1>
    <p class="text-blue-100">Match your resume with job descriptions using advanced AI algorithms</p>
    <div class="flex items-center gap-6 mt-4">
      <div class="text-sm text-blue-100">Enhanced ATS Algorithms</div>
      <label class="flex items-center gap-2 text-sm">
        <input type="checkbox" bind:checked={$useBackend} class="rounded" />
        Use Backend ATS Service
      </label>
    </div>
  </div>
</header>

{#if $errorMsg}
  <div class="max-w-7xl mx-auto px-8 mb-6">
    <div class="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
      <div class="flex">
        <svg class="w-5 h-5 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
        </svg>
        {$errorMsg}
      </div>
    </div>
  </div>
{/if}

<!-- Main Content Area -->
<div class="max-w-7xl mx-auto px-8">
  <!-- Job URL Input -->
  <div class="mb-6 bg-white rounded-lg shadow-sm border border-gray-200 p-4">
    <div class="flex gap-3">
      <input 
        type="text" 
        placeholder="Paste job posting URL to scrape..." 
        bind:value={jobUrl} 
        class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
      />
      <button 
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
        on:click={handleJobScrape} 
        disabled={loadingJob || !jobUrl}
      >
        {#if loadingJob}
          <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Scraping...
        {:else}
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
          </svg>
          Scrape Job
        {/if}
      </button>
    </div>
  </div>

  <!-- Side-by-Side Layout -->
  <div class="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-8">
    <!-- Job Posting Section -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold text-gray-900">Job Posting</h2>
          <div class="flex items-center gap-2">
            <button 
              class="px-3 py-1.5 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors flex items-center gap-1"
              on:click={toggleJobEditor}
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
              </svg>
              {showJobEditor ? 'View' : 'Edit'}
            </button>
          </div>
        </div>
      </div>

      <div class="p-6">
        {#if showJobEditor}
          <!-- Job Editor -->
          <div class="space-y-4">
            <RichTextEditor
              bind:value={jobEditorContent}
              placeholder="Paste or edit job description here..."
              height="400px"
            />
            <div class="flex gap-3">
              <button 
                class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                on:click={saveJobChanges}
              >
                Save Changes
              </button>
              <button 
                class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition-colors"
                on:click={toggleJobEditor}
              >
                Cancel
              </button>
            </div>
          </div>
        {:else}
          <!-- Job Display -->
          {#if $jobData}
            <JobPostingDisplay jobData={$jobData} atsResults={$myAts} />
          {:else}
            <div class="text-center py-12 text-gray-500">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6"></path>
              </svg>
              <p class="text-lg font-medium">No Job Posting</p>
              <p class="text-sm">Paste a job URL above or enter job description to get started</p>
            </div>
          {/if}
        {/if}
      </div>
    </div>

    <!-- Resume Section -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold text-gray-900">Your Resume</h2>
          <div class="flex items-center gap-2">
            {#if $myResume}
              <button 
                class="px-3 py-1.5 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors flex items-center gap-1"
                on:click={toggleResumeEditor}
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
                {showResumeEditor ? 'View' : 'Edit'}
              </button>
              <button 
                class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors flex items-center gap-1"
                on:click={downloadResumeAsPdf}
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Download
              </button>
            {/if}
          </div>
        </div>
      </div>

      <div class="p-6">
        {#if !$myResume}
          <!-- Resume Upload -->
          <div class="text-center py-12">
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 hover:border-blue-400 transition-colors">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
              <p class="text-lg font-medium text-gray-900 mb-2">Upload your resume</p>
              <p class="text-sm text-gray-500 mb-4">Support for PDF and DOCX files</p>
              <input 
                type="file" 
                accept=".pdf,.docx" 
                on:change={handleResumeChange} 
                class="hidden" 
                id="resume-upload"
              />
              <label 
                for="resume-upload"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors cursor-pointer inline-flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                </svg>
                Choose File
              </label>
            </div>
          </div>
        {:else if showResumeEditor}
          <!-- Resume Editor -->
          <div class="space-y-4">
            <RichTextEditor
              bind:value={resumeEditorContent}
              placeholder="Edit your resume content..."
              height="400px"
            />
            <div class="flex gap-3">
              <button 
                class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                on:click={saveResumeChanges}
              >
                Save Changes
              </button>
              <button 
                class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition-colors"
                on:click={toggleResumeEditor}
              >
                Cancel
              </button>
            </div>
          </div>
        {:else}
          <!-- Resume Display -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span class="font-medium text-gray-900">{$myResume.name}</span>
              </div>
              {#if loadingResume}
                <div class="text-sm text-gray-500">Parsing...</div>
              {/if}
            </div>
            
            {#if resumePdfUrl}
              <!-- PDF Display -->
              <div class="border border-gray-200 rounded-lg overflow-hidden">
                <iframe 
                  src={resumePdfUrl} 
                  class="w-full h-96" 
                  title="Resume PDF"
                ></iframe>
              </div>
            {:else}
              <!-- Text Display -->
              <div class="bg-gray-50 border border-gray-200 rounded-lg p-4 max-h-96 overflow-y-auto">
                <pre class="text-sm text-gray-700 whitespace-pre-wrap font-mono">{$myResume.text}</pre>
              </div>
            {/if}
          </div>
        {/if}
      </div>
    </div>
  </div>

  <!-- ATS Analysis Results -->
  {#if $myResume && $myAts}
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden mb-8">
      <div class="bg-gradient-to-r from-blue-50 to-purple-50 px-6 py-4 border-b border-gray-200">
        <h2 class="text-xl font-semibold text-gray-900">ATS Analysis Results</h2>
      </div>
      
      <div class="p-6">
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <!-- Overall Score -->
          <div class="text-center">
            <div class="text-4xl font-bold text-blue-600 mb-2">{$myAts.overall_score}%</div>
            <div class="text-sm text-gray-600">Overall Score</div>
            <div class="mt-2">
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-blue-600 h-2 rounded-full transition-all duration-500" style="width: {$myAts.overall_score}%"></div>
              </div>
            </div>
          </div>

          <!-- Keyword Match -->
          <div class="text-center">
            <div class="text-2xl font-bold text-green-600 mb-2">
              {$myAts.keyword_analysis.required.matched.length + $myAts.keyword_analysis.preferred.matched.length}
            </div>
            <div class="text-sm text-gray-600">Keywords Matched</div>
            <div class="text-xs text-gray-500 mt-1">
              {$myAts.keyword_analysis.required.matched.length} required, {$myAts.keyword_analysis.preferred.matched.length} preferred
            </div>
          </div>

          <!-- Missing Keywords -->
          <div class="text-center">
            <div class="text-2xl font-bold text-red-600 mb-2">
              {$myAts.keyword_analysis.required.missing.length + $myAts.keyword_analysis.preferred.missing.length}
            </div>
            <div class="text-sm text-gray-600">Keywords Missing</div>
            <div class="text-xs text-gray-500 mt-1">
              {$myAts.keyword_analysis.required.missing.length} required, {$myAts.keyword_analysis.preferred.missing.length} preferred
            </div>
          </div>

          <!-- Confidence -->
          <div class="text-center">
            <div class="text-2xl font-bold text-purple-600 mb-2">{$myAts.confidence}%</div>
            <div class="text-sm text-gray-600">Analysis Confidence</div>
          </div>
        </div>

        <!-- Detailed Breakdown -->
        <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h3 class="text-lg font-semibold mb-4 text-green-700">Matched Keywords</h3>
            <div class="space-y-3">
              {#if $myAts.keyword_analysis.required.matched.length}
                <div>
                  <div class="font-medium text-green-600 mb-2">Required ({$myAts.keyword_analysis.required.matched.length})</div>
                  <div class="flex flex-wrap gap-2">
                    {#each $myAts.keyword_analysis.required.matched as keyword}
                      <span class="px-2 py-1 bg-green-100 text-green-800 rounded-md text-sm font-medium">{keyword}</span>
                    {/each}
                  </div>
                </div>
              {/if}
              {#if $myAts.keyword_analysis.preferred.matched.length}
                <div>
                  <div class="font-medium text-blue-600 mb-2">Preferred ({$myAts.keyword_analysis.preferred.matched.length})</div>
                  <div class="flex flex-wrap gap-2">
                    {#each $myAts.keyword_analysis.preferred.matched as keyword}
                      <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded-md text-sm font-medium">{keyword}</span>
                    {/each}
                  </div>
                </div>
              {/if}
            </div>
          </div>

          <div>
            <h3 class="text-lg font-semibold mb-4 text-red-700">Missing Keywords</h3>
            <div class="space-y-3">
              {#if $myAts.keyword_analysis.required.missing.length}
                <div>
                  <div class="font-medium text-red-600 mb-2">Required ({$myAts.keyword_analysis.required.missing.length})</div>
                  <div class="flex flex-wrap gap-2">
                    {#each $myAts.keyword_analysis.required.missing as keyword}
                      <span class="px-2 py-1 bg-red-100 text-red-800 rounded-md text-sm font-medium">{keyword}</span>
                    {/each}
                  </div>
                </div>
              {/if}
              {#if $myAts.keyword_analysis.preferred.missing.length}
                <div>
                  <div class="font-medium text-orange-600 mb-2">Preferred ({$myAts.keyword_analysis.preferred.missing.length})</div>
                  <div class="flex flex-wrap gap-2">
                    {#each $myAts.keyword_analysis.preferred.missing as keyword}
                      <span class="px-2 py-1 bg-orange-100 text-orange-800 rounded-md text-sm font-medium">{keyword}</span>
                    {/each}
                  </div>
                </div>
              {/if}
            </div>
          </div>
        </div>

        <!-- Score Breakdown -->
        <div class="mt-8">
          <h3 class="text-lg font-semibold mb-4">Detailed Score Breakdown</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-4">
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium">Keyword Match</span>
                  <span class="text-sm font-bold text-blue-600">{$myAts.keyword_score}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-blue-600 h-2 rounded-full transition-all duration-500" style="width: {$myAts.keyword_score}%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium">Semantic Analysis</span>
                  <span class="text-sm font-bold text-green-600">{$myAts.semantic_score}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-green-600 h-2 rounded-full transition-all duration-500" style="width: {$myAts.semantic_score}%"></div>
                </div>
              </div>
            </div>
            <div class="space-y-4">
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium">Format & Structure</span>
                  <span class="text-sm font-bold text-purple-600">{$myAts.format_score}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-purple-600 h-2 rounded-full transition-all duration-500" style="width: {$myAts.format_score}%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium">Experience Match</span>
                  <span class="text-sm font-bold text-orange-600">{$myAts.experience_score}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-orange-600 h-2 rounded-full transition-all duration-500" style="width: {$myAts.experience_score}%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Improvement Suggestions -->
        {#if $myAts.improvements.critical.length || $myAts.improvements.important.length || $myAts.improvements.optional.length}
          <div class="mt-8">
            <h3 class="text-lg font-semibold mb-4">Improvement Suggestions</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              {#if $myAts.improvements.critical.length}
                <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                  <h4 class="font-semibold text-red-700 mb-3 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                    </svg>
                    Critical
                  </h4>
                  <ul class="space-y-2 text-sm">
                    {#each $myAts.improvements.critical as suggestion}
                      <li class="text-red-700 flex items-start gap-2">
                        <span class="w-1.5 h-1.5 bg-red-500 rounded-full mt-2 flex-shrink-0"></span>
                        {suggestion}
                      </li>
                    {/each}
                  </ul>
                </div>
              {/if}
              
              {#if $myAts.improvements.important.length}
                <div class="bg-orange-50 border border-orange-200 rounded-lg p-4">
                  <h4 class="font-semibold text-orange-700 mb-3 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    Important
                  </h4>
                  <ul class="space-y-2 text-sm">
                    {#each $myAts.improvements.important as suggestion}
                      <li class="text-orange-700 flex items-start gap-2">
                        <span class="w-1.5 h-1.5 bg-orange-500 rounded-full mt-2 flex-shrink-0"></span>
                        {suggestion}
                      </li>
                    {/each}
                  </ul>
                </div>
              {/if}
              
              {#if $myAts.improvements.optional.length}
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 class="font-semibold text-blue-700 mb-3 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                    </svg>
                    Optional
                  </h4>
                  <ul class="space-y-2 text-sm">
                    {#each $myAts.improvements.optional as suggestion}
                      <li class="text-blue-700 flex items-start gap-2">
                        <span class="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
                        {suggestion}
                      </li>
                    {/each}
                  </ul>
                </div>
              {/if}
            </div>
          </div>
        {/if}
      </div>
    </div>
  {/if}
</div>
