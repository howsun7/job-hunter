import Container from 'react-bootstrap/Container';
import NavBar from './components/NavBar';
import JobList from './components/JobList';

function App() {
  return (
    <>
      <NavBar />
      <section className='mt-4'>
        <Container>
          <JobList />
        </Container> 
      </section>
    </>
  );
}

export default App;
