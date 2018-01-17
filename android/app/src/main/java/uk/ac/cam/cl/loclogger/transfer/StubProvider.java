package uk.ac.cam.cl.loclogger.transfer;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.database.Cursor;
import android.net.Uri;

/*
    We don't use a ContentProvider, but this is required by the sync framework.
 */

public class StubProvider extends ContentProvider {
    @Override public boolean onCreate() {
        return true;
    }

    @Override public String getType(Uri uri) {
        return null;
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs,
                        String sortOrder) {
        return null;
    }

    @Override public Uri insert(Uri uri, ContentValues values) {
        return null;
    }

    @Override public int delete(Uri uri, String selection, String[] selectionArgs) {
        return 0;
    }

    public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
        return 0;
    }
}