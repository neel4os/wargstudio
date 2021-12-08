from datetime import datetime
from app.models.organization import OrganizationReq, OrganizationRes


def test_OrganizationReq():
    fake_data = {"name": "fake_name", "description": "fake_description"}
    assert OrganizationReq(**fake_data).dict() == fake_data


def test_OrganizationRes():
    fake_data = {
        "name": "fake_name",
        "description": "fake_description",
        "organizationId": "fake_id",
        "version": "1",
        "creationTime": datetime.utcnow(),
        "lastModifiedTime": datetime.utcnow(),
    }
    assert OrganizationRes(**fake_data).dict() == fake_data
