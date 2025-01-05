"""Replicate API client implementation."""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import replicate

logger = logging.getLogger(__name__)


class ReplicateClient:
    """Client for interacting with the Replicate API."""

    def __init__(self, api_token: Optional[str] = None) -> None:
        """Initialize the Replicate client.

        Args:
            api_token: Replicate API token for authentication
        """
        self.client = None
        self.error = None

        if not api_token or not api_token.strip():
            self.error = "Replicate API token is required"
            return

        os.environ["REPLICATE_API_TOKEN"] = api_token
        self.client = replicate.Client()

    def list_models(self, owner: Optional[str] = None, cursor: Optional[str] = None) -> Dict[str, Any]:
        """List available models on Replicate with pagination.

        Args:
            owner: Optional owner username to filter models
            cursor: Pagination cursor from previous response

        Returns:
            Dict containing models list, next cursor, and total count

        Raises:
            Exception: If the API request fails
        """
        try:
            # Get models collection with pagination
            models = self.client.models.list(cursor=cursor)

            # Get pagination info
            next_cursor = models.next_cursor if hasattr(models, "next_cursor") else None
            total_models = models.total if hasattr(models, "total") else None

            # Filter by owner if specified
            if owner:
                models = [m for m in models if m.owner == owner]

            # Format models with flattened structure
            formatted_models = []
            for model in models:
                model_data = {
                    "owner": model.owner,
                    "name": model.name,
                    "description": model.description,
                    "visibility": model.visibility,
                }

                # Add latest version info if available
                if model.latest_version:
                    model_data["latest_version_id"] = model.latest_version.id
                    model_data["latest_version_created_at"] = model.latest_version.created_at.isoformat()

                formatted_models.append(model_data)

            return {
                "models": formatted_models[:5],  # Limit to 5 models
                "next_cursor": next_cursor,
                "total_models": total_models,
            }

        except Exception as err:
            logger.error(f"Failed to list models: {str(err)}")
            raise Exception(f"Failed to list models: {str(err)}") from err

    def get_model_versions(self, model: str) -> List[Dict[str, Any]]:
        """Get available versions for a model.

        Args:
            model: Model identifier in format 'owner/model'

        Returns:
            List of model versions with their metadata

        Raises:
            ValueError: If the model is not found
            Exception: If the API request fails
        """
        try:
            # Get model
            model_obj = self.client.models.get(model)
            if not model_obj:
                raise ValueError(f"Model not found: {model}")

            # Get versions
            versions = model_obj.versions.list()

            # Return minimal version metadata
            return [
                {
                    "id": version.id,
                    "created_at": version.created_at.isoformat() if version.created_at else None,
                    "cog_version": version.cog_version,
                    "openapi_schema": version.openapi_schema,
                }
                for version in versions
            ]

        except ValueError as err:
            logger.error(f"Validation error: {str(err)}")
            raise
        except Exception as err:
            logger.error(f"Failed to get model versions: {str(err)}")
            raise Exception(f"Failed to get model versions: {str(err)}") from err

    def predict(self, model: str, input_data: Dict[str, Any], version: Optional[str] = None) -> Dict[str, Any]:
        """Run a prediction using a Replicate model.

        Args:
            model: Model identifier in format 'owner/model'
            input_data: Model-specific input parameters
            version: Optional model version hash

        Returns:
            Dict containing prediction details

        Raises:
            ValueError: If the model or version is not found
            Exception: If the prediction fails
        """
        try:
            # Get model
            model_obj = self.client.models.get(model)
            if not model_obj:
                raise ValueError(f"Model not found: {model}")

            # Get specific version or latest
            if version:
                model_version = model_obj.versions.get(version)
                if not model_version:
                    raise ValueError(f"Version not found: {version}")
            else:
                model_version = model_obj.latest_version

            # Create prediction
            prediction = model_version.predict(**input_data)

            # Return prediction details
            return {
                "id": prediction.id,
                "status": prediction.status,
                "output": prediction.output,
                "error": prediction.error,
                "created_at": prediction.created_at.isoformat() if prediction.created_at else None,
                "started_at": prediction.started_at.isoformat() if prediction.started_at else None,
                "completed_at": prediction.completed_at.isoformat() if prediction.completed_at else None,
            }

        except ValueError as err:
            logger.error(f"Validation error: {str(err)}")
            raise
        except Exception as err:
            logger.error(f"Prediction failed: {str(err)}")
            raise Exception(f"Prediction failed: {str(err)}") from err

    def get_prediction_status(self, prediction_id: str) -> Dict[str, Any]:
        """Get the status of a prediction.

        Args:
            prediction_id: ID of the prediction to check

        Returns:
            Dict containing current status and output of the prediction

        Raises:
            ValueError: If the prediction is not found
            Exception: If the API request fails
        """
        try:
            # Get prediction
            prediction = self.client.predictions.get(prediction_id)
            if not prediction:
                raise ValueError(f"Prediction not found: {prediction_id}")

            # Return prediction status and output
            return {
                "id": prediction.id,
                "status": prediction.status,
                "output": prediction.output,
                "error": prediction.error,
                "created_at": prediction.created_at.isoformat() if prediction.created_at else None,
                "started_at": prediction.started_at.isoformat() if prediction.started_at else None,
                "completed_at": prediction.completed_at.isoformat() if prediction.completed_at else None,
                "urls": prediction.urls,
                "metrics": prediction.metrics,
            }

        except ValueError as err:
            logger.error(f"Validation error: {str(err)}")
            raise
        except Exception as err:
            logger.error(f"Failed to get prediction status: {str(err)}")
            raise Exception(f"Failed to get prediction status: {str(err)}") from err
