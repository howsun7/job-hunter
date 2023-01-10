import Card from 'react-bootstrap/Card';

const JobCard = ({ job }) => {
  return (
    <Card className="mb-3">
      <Card.Body>
        <Card.Title>{job.title}</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">{job.company.name}</Card.Subtitle>
        <Card.Text>
          <span className="d-block">YOE required: {job.yoe_required}+</span>
          <span className="d-block">Location: {job.location}</span>
          <span className="d-block">Skills: {job.skills.map((skill, idx) => idx === 0 ? skill.name : `, ${skill.name}` )}</span>
        </Card.Text>
        <Card.Link href="{job.link}">job link</Card.Link>        
      </Card.Body>
    </Card>
  )
}

export default JobCard;