from uuid import uuid4
import httpx

class tts:
    def create(text: str, voice_name: str) -> dict:

        uuid_str = str(uuid4())

        response = httpx.post(
            "https://api.fakeyou.com/tts/inference",
            json={
                "inference_text": text,
                "tts_model_token": voice_name,
                "uuid_idempotency_token": uuid_str,
            },
        )

        uuid = None
        detail = None

        try:
            detail = response.json()["success"]

            if detail == False:
                detail = "That voice does not exist"

        except KeyError:
            pass

        try:
            uuid = response.json()["inference_job_token"]
        except KeyError:
            pass

        return {
            "detail": detail,
            "session": uuid,
        }

    def status(uuid: str) -> dict:
        

        response = httpx.get(f"https://api.fakeyou.com/tts/job/{uuid}")

        if response.json()["state"]["status"] == "attempt_failed":
            failed_at = response.json()["state"]["status"]
        elif response.json()["state"]["status"] == "complete_failure":
            failed_at = response.json()["state"]["status"]
        else:
            failed_at = None

        if response.json()["state"]["maybe_public_bucket_wav_audio_path"] is not None:
            path = "https://storage.googleapis.com/vocodes-public" + str(
                response.json()["state"]["maybe_public_bucket_wav_audio_path"]
            )
        else:
            path = None

        return {
            "path": path,
            "failed_at": failed_at,
        }
