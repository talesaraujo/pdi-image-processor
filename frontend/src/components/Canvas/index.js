import { Container, Image, Row } from 'react-bootstrap'
import image from '../../temp/ufc.jpg'

export function Canvas() {
    return (
        <Container>
            <Row className="justify-content-md-center mt-5">
                <Image src={image} alt={`image-${image}`} ></Image>
            </Row>
        </Container>
    )
}
