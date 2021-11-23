import { api } from './api'

export function imageUpload(img) {
    api.post(
        '/image',
        img,
        {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }
    )
    .then((response) => console.log(response))
    .catch((error) => console.log(error))
}
