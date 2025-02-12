"""
Copyright start
MIT License
Copyright (c) 2025 Fortinet Inc
Copyright end
"""

ASSET_SORT_BY = {
    "ID": "id",
    "Created At": "createdAt",
    "LastSeen At": "lastSeenAt",
    "First Address ID": 'firstAddressId',
    "First Address Type": "firstAddressType",
    "First Address Network ID": 'firstAddressNetworkId',
    "First Address Value": 'firstAddressValue',
    "Attribute": 'attribute'
}

NOTIFICATION_SORT = {
    "ID": "id",
    "Source": "source",
    "Type": "type",
    "Created At": "createdAt",
    "Occurred At": "occurredAt",
    "Severity": "severity",
    "Reviewed": "reviewed",
    "Retained": "retained",
    "Detector ID": "detectorId",
    "First Source IP": "firstSourceIp",
    "First Destination IP": "firstDestinationIp",
    "First Other IP": "firstOtherIp",
    "First Source Hostname": "firstSourceHostname",
    "First Destination Hostname": "firstDestinationHostname",
    "First Other Hostname": "firstOtherHostname",
    "Threat Framework": "threatFramework",
    "Threat Tactic ID": "threatTacticId",
    "Threat Tactic Name": "threatTacticName",
    "Threat Technique ID": "threatTechniqueId",
    "Threat Technique Name": "threatTechniqueName",
    "Last Seen At": "lastSeenAt",
    "Packet Capture State": "packetCaptureState"
}

NOTIFICATION_GROUP_BY = {
    "Type": "type",
    "Source": "source",
    "Severity": "severity",
    "Asset ID": "assetId",
    "Reviewed": "reviewed",
    "Retained": "retained",
    "Detector ID": "detectorId",
    "Matched Rule ID": "matchedRuleId",
    "CreatedAt Month": "createdAtMonth",
    "CreatedAt Day": "createdAtDay",
    "CreatedAt Hour": "createdAtHour",
    "OccurredAt Month": "occurredAtMonth",
    "OccurredAt Day": "occurredAtDay",
    "OccurredAt Hour": "occurredAtHour",
    "State": "state",
    "Metadata Type": "metadataType",
    "Metadata Asset ID": "metadataAssetId",
    "Metadata Source Asset ID": "metadataSourceAssetId",
    "Parent Notification ID": "parentNotificationId"
}
