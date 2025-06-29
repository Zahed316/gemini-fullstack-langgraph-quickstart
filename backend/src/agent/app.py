"""FastAPI application exposing the LangGraph agent and frontend assets."""

# mypy: disable - error - code = "no-untyped-def,misc"
import logging
import pathlib

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

# Define the FastAPI app
app = FastAPI()
logger = logging.getLogger(__name__)


def create_frontend_router(build_dir="../frontend/dist"):
    """Create a router to serve the React frontend.

    Args:
        build_dir: Path to the React build directory relative to this file.

    Returns:
        A Starlette application serving the frontend.
    """
    build_path = pathlib.Path(__file__).parent.parent.parent / build_dir

    if not build_path.is_dir() or not (build_path / "index.html").is_file():
        logger.warning(
            build_path,
        )
        # Return a dummy router if build isn't ready
        from starlette.routing import Route

        async def dummy_frontend(request):
            """Return a 503 response when the frontend build is missing."""
            return Response(
                "Frontend not built. Run 'npm run build' in the frontend directory.",
                media_type="text/plain",
                status_code=503,
            )

        return Route("/{path:path}", endpoint=dummy_frontend)

    return StaticFiles(directory=build_path, html=True)


# Mount the frontend under /app to not conflict with the LangGraph API routes
app.mount(
    "/app",
    create_frontend_router(),
    name="frontend",
)
