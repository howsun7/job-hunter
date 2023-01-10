import { useState, useEffect } from 'react';
import JobCard from './JobCard';


const JobList = () => {

  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    fetch('http://localhost:3030/api/jobs')
      .then(res => res.json())
      .then(
        (result) => {
          setJobs(result);          
        } 
      )
  }, [])

  return (
    <>
      {
        jobs.length !== 0
        ? jobs.map(job => (
          <JobCard job={job} key={job.id} />  
        ))
        : <h2>no job data available</h2>
      }
    </>
  )
}

export default JobList;